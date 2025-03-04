import logging
from enum import StrEnum, auto
from typing import Iterator, Self

from cadenza.errors import ParseError
from cadenza.interval import Interval
from cadenza.scale_type import ScaleType

logger = logging.getLogger(__name__)


class DiatonicMode(StrEnum):
    Ionian = auto()
    Dorian = auto()
    Phrygian = auto()
    Lydian = auto()
    Mixolydian = auto()
    Aeolian = auto()
    Locrian = auto()

    def to_int(self) -> int:  # noqa: PLR0911
        match self:
            case DiatonicMode.Ionian:
                return 0
            case DiatonicMode.Dorian:
                return 1
            case DiatonicMode.Phrygian:
                return 2
            case DiatonicMode.Lydian:
                return 3
            case DiatonicMode.Mixolydian:
                return 4
            case DiatonicMode.Aeolian:
                return 5
            case DiatonicMode.Locrian:
                return 6

    @classmethod
    def from_int(cls, mode_int: int) -> "DiatonicMode":
        mapping = {
            0: cls.Ionian,
            1: cls.Dorian,
            2: cls.Phrygian,
            3: cls.Lydian,
            4: cls.Mixolydian,
            5: cls.Aeolian,
            6: cls.Locrian,
        }
        if mode_int not in mapping:
            msg = f"Invalid mode: {mode_int}"
            raise ParseError(msg)
        return mapping[mode_int]

    def get_semitone_sequence(self) -> list[int]:  # noqa: PLR0911
        # NOTE: Each set of intervals for a mode is a rotation of the previous.
        match self:
            case DiatonicMode.Ionian:
                return [2, 2, 1, 2, 2, 2, 1]  # W W H W W W H
            case DiatonicMode.Dorian:
                return [2, 1, 2, 2, 2, 1, 2]  # W H W W W H W
            case DiatonicMode.Phrygian:
                return [1, 2, 2, 2, 1, 2, 2]  # H W W W H W W
            case DiatonicMode.Lydian:
                return [2, 2, 2, 1, 2, 2, 1]  # W W W H W W H
            case DiatonicMode.Mixolydian:
                return [2, 2, 1, 2, 2, 1, 2]  # W W H W W H W
            case DiatonicMode.Aeolian:
                return [2, 1, 2, 2, 1, 2, 2]  # W H W W H W W
            case DiatonicMode.Locrian:
                return [1, 2, 2, 1, 2, 2, 2]  # H W W H W W W

    def get_intervals(self) -> list[Interval]:
        return list(self.iter_intervals())

    def iter_intervals(self) -> Iterator[Interval]:
        yield Interval.Unison
        interval_int = 0
        for semitones in self.get_semitone_sequence():
            interval_int += semitones
            yield Interval.from_int(interval_int)

    def to_scale_type(self) -> ScaleType:
        match self:
            case DiatonicMode.Ionian:
                return ScaleType.Major
            case DiatonicMode.Aeolian:
                return ScaleType.NaturalMinor
            case _:
                msg = f"No known scale for the diatonic mode: {self}"
                raise ValueError(msg)

    @classmethod
    def from_scale_type(cls, scale_type: ScaleType) -> "DiatonicMode":
        match scale_type:
            case ScaleType.Major:
                return DiatonicMode.Ionian
            case ScaleType.NaturalMinor:
                return DiatonicMode.Aeolian

    def to_written(self) -> str:
        return self.value

    def to_str(self, convert_to_quality: bool = True) -> str:
        if convert_to_quality:
            if self == DiatonicMode.Ionian:
                return "major"
            if self == DiatonicMode.Aeolian:
                return "minor"
        return self.value

    @classmethod
    def from_str(cls, mode_str: str) -> Self:
        if mode_str == "major":
            mode_str = "Ionian"

        if mode_str == "minor":
            mode_str = "Aeolian"

        return cls[mode_str]

    def __str__(self) -> str:
        return self.to_written()

    def __repr__(self) -> str:
        return self.value
