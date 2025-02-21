import logging
import re
from typing import Optional, Self

from pydantic import BaseModel

from cadenza.alteration import Alteration
from cadenza.errors import ParseError
from cadenza.extension import Extension
from cadenza.interval import Interval
from cadenza.note import Note
from cadenza.quality import Quality
from cadenza.scale_degree import ScaleDegree

logger = logging.getLogger(__name__)


class Chord(BaseModel):
    root: Note
    quality: Quality
    extension: Optional[Extension] = None
    alteration: Optional[Alteration] = None
    bass: Optional[Note] = None

    @classmethod
    def from_str(cls, chord_str: str) -> Self:
        regex = (
            r"^([A-Ga-g](♯|#|♭|b)?)"  # Root
            r"(m|min|dim|aug|\+|ø|halfdim|sus2|sus4)?"  # Quality
            r"(7|maj7|9|11|13)?"  # Extension
            r"((♯|#|♭|b|sharp|flat|add)?\d+)?"  # Alteration
            r"(/([A-Ga-g](♯|#|♭|b)?))?$"  # Optional bass note
        )

        match = re.match(regex, chord_str)
        if not match:
            msg = f"Failed to parse chord string: {chord_str}"
            raise ParseError(msg)
        root_str, _, quality_str, extension_str, alteration_str, _, _, bass_str, _ = match.groups()

        root = Note.from_str(root_str)
        quality = Quality.from_str(quality_str) if quality_str else Quality.Major
        extension = Extension.from_str(extension_str) if extension_str else None
        alteration = Alteration.from_str(alteration_str) if alteration_str else None
        bass = Note.from_str(bass_str) if bass_str else None
        return cls(root=root, quality=quality, extension=extension, alteration=alteration, bass=bass)

    def __str__(self) -> str:
        extension_str = self.extension.to_str() if self.extension else ""
        alterations_str = self.alteration.to_str() if self.alteration else ""
        bass_str = f"/{self.bass.to_str()}" if self.bass else ""
        return f"{self.root}{self.quality}{extension_str}{alterations_str}{bass_str}"

    @classmethod
    def from_scale_degree(cls, tonic: "Chord", scale_degree: ScaleDegree) -> Self:
        match tonic.quality:
            case Quality.Major:
                return {
                    ScaleDegree.Tonic: cls(root=tonic.root + 0, quality=Quality.Major),
                    ScaleDegree.Supertonic: cls(root=tonic.root + 2, quality=Quality.Minor),
                    ScaleDegree.Mediant: cls(root=tonic.root + 4, quality=Quality.Minor),
                    ScaleDegree.Subdominant: cls(root=tonic.root + 5, quality=Quality.Major),
                    ScaleDegree.Dominant: cls(root=tonic.root + 7, quality=Quality.Major),
                    ScaleDegree.Submediant: cls(root=tonic.root + 9, quality=Quality.Minor),
                    ScaleDegree.LeadingTone: cls(root=tonic.root + 11, quality=Quality.Diminished),
                }[scale_degree]
            case Quality.Minor:
                return {
                    ScaleDegree.Tonic: cls(root=tonic.root + 0, quality=Quality.Minor),
                    ScaleDegree.Supertonic: cls(root=tonic.root + 2, quality=Quality.Diminished),
                    ScaleDegree.Mediant: cls(root=tonic.root + 3, quality=Quality.Major),
                    ScaleDegree.Subdominant: cls(root=tonic.root + 5, quality=Quality.Minor),
                    ScaleDegree.Dominant: cls(root=tonic.root + 7, quality=Quality.Minor),
                    ScaleDegree.Submediant: cls(root=tonic.root + 8, quality=Quality.Major),
                    ScaleDegree.LeadingTone: cls(root=tonic.root + 10, quality=Quality.Minor),
                }[scale_degree]
            case _:
                msg = f"Getting chords by degree for quality {tonic.quality.to_written()} is not supported"
                raise ValueError(msg)

    def transpose(self, semitones: int) -> "Chord":
        new_root = self.root + semitones
        new_bass = self.bass + semitones if self.bass else None
        return Chord(
            root=new_root,
            quality=self.quality,
            extension=self.extension,
            alteration=self.alteration,
            bass=new_bass,
        )

    def to_function(self, tonic: "Chord") -> str:
        tonic_root = tonic.root

        interval_num = (self.root.to_index() - tonic_root.to_index()) % 12
        interval = Interval.from_int(interval_num)
        try:
            scale_degree = ScaleDegree.from_interval(interval)
        except ValueError as exc:
            msg = f"Failed to convert chord {self} to a scale degree: {exc}"
            logger.debug(msg)
            return str(self)
        function_map = {
            ScaleDegree.Tonic: "I",
            ScaleDegree.Supertonic: "II",
            ScaleDegree.Mediant: "III",
            ScaleDegree.Subdominant: "IV",
            ScaleDegree.Dominant: "V",
            ScaleDegree.Submediant: "VI",
            ScaleDegree.LeadingTone: "VII",
        }
        func = function_map[scale_degree]
        ret = func
        if self.quality in [Quality.Minor, Quality.Diminished]:
            ret = ret.lower()
        if self.quality == Quality.Diminished:
            ret += "°"
        if self.quality == Quality.Augmented:
            ret += "+"
        if self.quality == Quality.SusTwo:
            ret += "sus2"
        if self.quality == Quality.SusFour:
            ret += "sus4"
        if self.extension == Extension.Seven:
            ret += "7"
        if self.extension == Extension.MajorSeven:
            ret += "maj7"

        if self.bass is not None:
            base_interval_num = (self.bass.to_index() - tonic_root.to_index()) % 12
            base_interval = Interval.from_int(base_interval_num)
            try:
                base_scale_degree = ScaleDegree.from_interval(base_interval)
            except ValueError as exc:
                msg = f"Failed to convert chord {self} bass to a scale degree: {exc}"
                logger.debug(msg)
                return str(self)
            base_func = function_map[base_scale_degree]
            ret += f"/{base_func}"

        return ret

    def to_key(self) -> str:
        match self.quality:
            case Quality.Major:
                return self.root.to_str() + " major"
            case Quality.Minor:
                return self.root.to_str() + " minor"
            case _:
                msg = f"The chord {self} could not be converted to a key"
                raise ValueError(msg)
