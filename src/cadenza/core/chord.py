import logging
import re
from typing import Optional, Self

from pydantic import BaseModel

from cadenza.core.alteration import Alteration
from cadenza.core.constants import N_NOTES
from cadenza.core.errors import ParseError
from cadenza.core.extension import Extension
from cadenza.core.interval import Interval
from cadenza.core.note import Note
from cadenza.core.quality import Quality

logger = logging.getLogger(__name__)


class Chord(BaseModel):
    root: Note
    quality: Quality
    extension: Optional[Extension] = None
    alteration: Optional[Alteration] = None
    bass: Optional[Note] = None

    @classmethod
    def from_str(cls, chord_str: str) -> Self:
        # NOTE: A doubled flat written out in full collides with the flattened alterations, so Ebb9
        # is read as an E♭ with a flattened ninth rather than an E𝄫 ninth. Only ♭5 and ♭9 can follow,
        # so Bbb6 is still a B𝄫 with an added sixth. Nothing may follow a sharp, and the
        # single-glyph forms are unambiguous, so neither needs the guard.
        accidental = r"(𝄪|𝄫|##|♯♯|bb(?![59])|♭♭(?![59])|♯|#|♭|b)?"
        regex = (
            rf"^([A-Ga-g]{accidental})"  # Root
            r"(m|dim|\°|aug|\+|\ø|halfdim|5)?"  # Quality pre
            r"(7|maj7|9|maj9|11|13)?"  # Extension
            r"((♯|#|♭|b|sharp|flat|add)\d+|[246])?"  # Alteration
            r"(sus2|sus4)?"  # Quality post
            rf"(/([A-Ga-g]{accidental}))?$"  # Optional bass note
        )

        match = re.match(regex, chord_str)
        if not match:
            msg = f"Failed to parse chord string: {chord_str}"
            raise ParseError(msg)
        root_str, _, quality_pre_str, extension_str, alteration_str, _, quality_post_str, _, bass_str, _ = (
            match.groups()
        )

        root = Note.from_str(root_str)
        if quality_pre_str:
            quality = Quality.from_str(quality_pre_str)
        elif quality_post_str:
            quality = Quality.from_str(quality_post_str)
        else:
            quality = Quality.Major
        extension = Extension.from_str(extension_str) if extension_str else None
        alteration = Alteration.from_str(alteration_str) if alteration_str else None
        bass = Note.from_str(bass_str) if bass_str else None
        return cls(root=root, quality=quality, extension=extension, alteration=alteration, bass=bass)

    def _get_quality_intervals(self) -> list[Interval]:  # noqa: PLR0911
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
            case Quality.Power:
                # NOTE: A power chord is just the root and perfect fifth, with no third.
                return [Interval.PerfectFifth]

    def _get_extension_intervals(self) -> list[Interval]:  # noqa: PLR0911
        if not self.extension:
            return []
        match self.extension:
            case Extension.Seven:
                return [Interval.MinorSeventh]
            case Extension.MajorSeven:
                return [Interval.MajorSeventh]
            case Extension.Nine:
                # NOTE: The 9 chord includes all previous extensions (the 7th).
                return [Interval.MinorSeventh, Interval.MajorNinth]
            case Extension.MajorNine:
                # NOTE: The maj9 chord includes all previous extensions (the 7th).
                return [Interval.MajorSeventh, Interval.MajorNinth]
            case Extension.Eleven:
                # NOTE: The 11 chord includes all previous extensions (the 7th and 9th).
                return [Interval.MinorSeventh, Interval.MajorNinth, Interval.PerfectEleventh]
            case Extension.Thirteen:
                # NOTE: Often the 13 chord is played without the 11th,
                # though both are accepted voicings.
                return [Interval.MinorSeventh, Interval.MajorNinth, Interval.MajorThirteenth]

    def _update_intervals_from_alteration(self, intervals: list[Interval]) -> None:
        if not self.alteration:
            return
        match self.alteration:
            case Alteration.AddTwo:
                intervals.append(Interval.MajorSecond)
            case Alteration.AddFour:
                intervals.append(Interval.PerfectFourth)
            case Alteration.AddSix:
                match self.quality:
                    # NOTE: A power chord has no third, so it defaults to the major sixth.
                    case Quality.Major | Quality.Power:
                        intervals.append(Interval.MajorSixth)
                    case Quality.Minor:
                        intervals.append(Interval.MinorSixth)
                    case _:
                        msg = f"Invalid quality for add6: {self.quality}"
                        raise ValueError(msg)
            case Alteration.AddNine:
                intervals.append(Interval.MajorNinth)
            case Alteration.FlatFive:
                intervals.remove(Interval.PerfectFifth)
                intervals.append(Interval.Tritone)
            case Alteration.FlatNine:
                intervals.append(Interval.MinorNinth)

    def get_intervals(self) -> list[Interval]:
        intervals = [Interval.Unison, *self._get_quality_intervals(), *self._get_extension_intervals()]
        self._update_intervals_from_alteration(intervals)
        return intervals

    def contains_pitch_class(self, pitch_class: int) -> bool:
        return (pitch_class - self.root.to_integer()) % N_NOTES in {
            interval.to_int() % N_NOTES for interval in self.get_intervals()
        }

    def to_str(self, symbols: bool = True) -> str:
        extension_str = self.extension.to_str() if self.extension else ""
        alterations_str = self.alteration.to_str(symbols=symbols) if self.alteration else ""
        bass_str = f"/{self.bass.to_str(symbols=symbols)}" if self.bass else ""
        ret = self.root.to_str(symbols=symbols)
        if self.quality.is_prefix():
            ret += self.quality.to_str(symbols=symbols)
        ret += extension_str
        ret += alterations_str
        if self.quality.is_suffix():
            ret += self.quality.to_str(symbols=symbols)
        ret += bass_str
        return ret

    def __str__(self) -> str:
        return self.to_str()
