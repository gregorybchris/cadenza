import logging
import re
from typing import Optional, Self

from pydantic import BaseModel

from cadenza.alteration import Alteration
from cadenza.errors import ParseError
from cadenza.extension import Extension
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
            r"(add\d+|7|maj7|9|11|13)?"  # Extension
            r"([♯#♭b]\d+)?"  # Alteration
            r"(/([A-Ga-g](♯|#|♭|b)?))?$"  # Optional bass note
        )

        match = re.match(regex, chord_str)
        if not match:
            msg = f"Failed to parse chord string: {chord_str}"
            raise ParseError(msg)
        root_str, _, quality_str, extension_str, alteration_str, _, bass_str, _ = match.groups()

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
        root = tonic.root
        minor = Quality.Minor
        major = Quality.Major
        diminished = Quality.Diminished
        match tonic.quality:
            case Quality.Major:
                return {
                    ScaleDegree.Tonic: cls(root=root + 0, quality=major),
                    ScaleDegree.Supertonic: cls(root=root + 2, quality=minor),
                    ScaleDegree.Mediant: cls(root=root + 4, quality=minor),
                    ScaleDegree.Subdominant: cls(root=root + 5, quality=major),
                    ScaleDegree.Dominant: cls(root=root + 7, quality=major),
                    ScaleDegree.Submediant: cls(root=root + 9, quality=minor),
                    ScaleDegree.LeadingTone: cls(root=root + 11, quality=diminished),
                }[scale_degree]
            case Quality.Minor:
                return {
                    ScaleDegree.Tonic: cls(root=root + 0, quality=minor),
                    ScaleDegree.Supertonic: cls(root=root + 2, quality=diminished),
                    ScaleDegree.Mediant: cls(root=root + 3, quality=major),
                    ScaleDegree.Subdominant: cls(root=root + 5, quality=minor),
                    ScaleDegree.Dominant: cls(root=root + 7, quality=minor),
                    ScaleDegree.Submediant: cls(root=root + 8, quality=major),
                    ScaleDegree.LeadingTone: cls(root=root + 10, quality=minor),
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
