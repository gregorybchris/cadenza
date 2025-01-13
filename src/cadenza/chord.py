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

    @classmethod
    def from_str(cls, chord_str: str) -> Self:
        regex = (
            r"^([A-Ga-g](♯|#|♭|b)?)"  # Root
            r"(m|min|dim|aug|\+|ø|halfdim|sus2|sus4)?"  # Quality
            r"(add\d+|7|maj7|9|11|13)?"  # Extension
            r"([♯#♭b]\d+)?$"  # Alteration
        )
        match = re.match(regex, chord_str)
        if not match:
            msg = f"Failed to parse chord string: {chord_str}"
            raise ParseError(msg)
        root_str, _, quality_str, extension_str, alteration_str = match.groups()

        root = Note.from_str(root_str)
        quality = Quality.from_str(quality_str) if quality_str else Quality.Major
        extension = Extension.from_str(extension_str) if extension_str else None
        alteration = Alteration.from_str(alteration_str) if alteration_str else None
        return cls(root=root, quality=quality, extension=extension, alteration=alteration)

    def __str__(self) -> str:
        extension_str = "" if self.extension is None else self.extension.to_str()
        alterations_str = "" if self.alteration is None else self.alteration.to_str()
        return f"{self.root}{self.quality}{extension_str}{alterations_str}"

    def _get_intervals_from_quality(self) -> list[Interval]:  # noqa: PLR0911
        match self.quality:
            case Quality.Major:
                return [Interval.MajorThird, Interval.PerfectFifth]
            case Quality.Minor:
                return [Interval.MinorThird, Interval.PerfectFifth]
            case Quality.Diminished:
                return [Interval.MinorThird, Interval.Tritone]
            case Quality.Augmented:
                return [Interval.MajorThird, Interval.MinorSixth]
            case Quality.HalfDiminished:
                return [Interval.MinorThird, Interval.Tritone, Interval.MinorSeventh]
            case Quality.SusTwo:
                return [Interval.MajorSecond, Interval.PerfectFifth]
            case Quality.SusFour:
                return [Interval.PerfectFourth, Interval.PerfectFifth]

    def _get_intervals_from_extension(self) -> list[Interval]:
        if not self.extension:
            return []
        match self.extension:
            case Extension.Seven:
                return [Interval.MinorSeventh]
            case Extension.MajorSeven:
                return [Interval.MajorSeventh]
            case Extension.AddNine:
                return [Interval.MajorSecond]
            case Extension.AddEleven:
                return [Interval.PerfectFourth]
            case Extension.AddThirteen:
                return [Interval.MajorSixth]

    def _get_intervals_from_alteration(self) -> list[Interval]:
        if not self.alteration:
            return []
        match self.alteration:
            case Alteration.FlatFive:
                return [Interval.Tritone]

    def get_intervals(self) -> list[Interval]:
        intervals = [Interval.Unison]
        intervals += self._get_intervals_from_quality()
        intervals += self._get_intervals_from_extension()
        intervals += self._get_intervals_from_alteration()
        return intervals

    def get_notes(self) -> list[Note]:
        intervals = self.get_intervals()
        return [self.root + interval.to_int() for interval in intervals]

    @classmethod
    def from_scale_degree(cls, tonic: "Chord", scale_degree: ScaleDegree) -> Self:
        root = tonic.root
        minor = Quality.Minor
        major = Quality.Major
        diminished = Quality.Diminished
        match tonic.quality:
            case Quality.Major:
                return {
                    ScaleDegree.Tonic: cls(root=root, quality=major),
                    ScaleDegree.Supertonic: cls(root=root + 2, quality=minor),
                    ScaleDegree.Mediant: cls(root=root + 4, quality=minor),
                    ScaleDegree.Subdominant: cls(root=root + 5, quality=major),
                    ScaleDegree.Dominant: cls(root=root + 7, quality=major),
                    ScaleDegree.Submediant: cls(root=root + 9, quality=minor),
                    ScaleDegree.LeadingTone: cls(root=root + 10, quality=diminished),
                }[scale_degree]
            case Quality.Minor:
                return {
                    ScaleDegree.Tonic: cls(root=root, quality=minor),
                    ScaleDegree.Supertonic: cls(root=root + 2, quality=diminished),
                    ScaleDegree.Mediant: cls(root=root + 3, quality=major),
                    ScaleDegree.Subdominant: cls(root=root + 5, quality=minor),
                    ScaleDegree.Dominant: cls(root=root + 6, quality=minor),
                    ScaleDegree.Submediant: cls(root=root + 8, quality=major),
                    ScaleDegree.LeadingTone: cls(root=root + 10, quality=minor),
                }[scale_degree]
            case _:
                msg = f"Getting chords by degree for quality {tonic.quality.to_written()} is not supported"
                raise ValueError(msg)
