import logging
from enum import StrEnum, auto

from cadenza.errors import ParseError

logger = logging.getLogger(__name__)


class Interval(StrEnum):
    Unison = auto()
    MinorSecond = auto()
    MajorSecond = auto()
    MinorThird = auto()
    MajorThird = auto()
    PerfectFourth = auto()
    Tritone = auto()
    PerfectFifth = auto()
    MinorSixth = auto()
    MajorSixth = auto()
    MinorSeventh = auto()
    MajorSeventh = auto()
    Octave = auto()
    MinorNinth = auto()
    MajorNinth = auto()
    MinorTenth = auto()
    MajorTenth = auto()
    PerfectEleventh = auto()
    AugmentedEleventh = auto()
    PerfectTwelfth = auto()
    MinorThirteenth = auto()
    MajorThirteenth = auto()

    def to_written(self) -> str:  # noqa: PLR0911, PLR0912
        match self:
            case Interval.Unison:
                return "unison"
            case Interval.MinorSecond:
                return "minor second"
            case Interval.MajorSecond:
                return "major second"
            case Interval.MinorThird:
                return "minor third"
            case Interval.MajorThird:
                return "major third"
            case Interval.PerfectFourth:
                return "perfect fourth"
            case Interval.Tritone:
                return "tritone"
            case Interval.PerfectFifth:
                return "perfect fifth"
            case Interval.MinorSixth:
                return "minor sixth"
            case Interval.MajorSixth:
                return "major sixth"
            case Interval.MinorSeventh:
                return "minor seventh"
            case Interval.MajorSeventh:
                return "major seventh"
            case Interval.Octave:
                return "octave"
            case Interval.MinorNinth:
                return "minor ninth"
            case Interval.MajorNinth:
                return "major ninth"
            case Interval.MinorTenth:
                return "minor tenth"
            case Interval.MajorTenth:
                return "major tenth"
            case Interval.PerfectEleventh:
                return "perfect eleventh"
            case Interval.AugmentedEleventh:
                return "augmented eleventh"
            case Interval.PerfectTwelfth:
                return "perfect twelfth"
            case Interval.MinorThirteenth:
                return "minor thirteenth"
            case Interval.MajorThirteenth:
                return "major thirteenth"

    @classmethod
    def from_str(cls, interval_str: str) -> "Interval":
        mapping = {
            "P1": cls.Unison,
            "m2": cls.MinorSecond,
            "M2": cls.MajorSecond,
            "m3": cls.MinorThird,
            "M3": cls.MajorThird,
            "P4": cls.PerfectFourth,
            "TT": cls.Tritone,
            "P5": cls.PerfectFifth,
            "m6": cls.MinorSixth,
            "M6": cls.MajorSixth,
            "m7": cls.MinorSeventh,
            "M7": cls.MajorSeventh,
            "P8": cls.Octave,
            "m9": cls.MinorNinth,
            "M9": cls.MajorNinth,
            "m10": cls.MinorTenth,
            "M10": cls.MajorTenth,
            "P11": cls.PerfectEleventh,
            "A11": cls.AugmentedEleventh,
            "P12": cls.PerfectTwelfth,
            "m13": cls.MinorThirteenth,
            "M13": cls.MajorThirteenth,
        }
        if interval_str not in mapping:
            msg = f"Invalid interval: {interval_str}"
            raise ParseError(msg)
        return mapping[interval_str]

    def to_str(self) -> str:  # noqa: PLR0911, PLR0912
        match self:
            case Interval.Unison:
                return "P1"
            case Interval.MinorSecond:
                return "m2"
            case Interval.MajorSecond:
                return "M2"
            case Interval.MinorThird:
                return "m3"
            case Interval.MajorThird:
                return "M3"
            case Interval.PerfectFourth:
                return "P4"
            case Interval.Tritone:
                return "TT"
            case Interval.PerfectFifth:
                return "P5"
            case Interval.MinorSixth:
                return "m6"
            case Interval.MajorSixth:
                return "M6"
            case Interval.MinorSeventh:
                return "m7"
            case Interval.MajorSeventh:
                return "M7"
            case Interval.Octave:
                return "P8"
            case Interval.MinorNinth:
                return "m9"
            case Interval.MajorNinth:
                return "M9"
            case Interval.MinorTenth:
                return "m10"
            case Interval.MajorTenth:
                return "M10"
            case Interval.PerfectEleventh:
                return "P11"
            case Interval.AugmentedEleventh:
                return "A11"
            case Interval.PerfectTwelfth:
                return "P12"
            case Interval.MinorThirteenth:
                return "m13"
            case Interval.MajorThirteenth:
                return "M13"

    def to_int(self) -> int:  # noqa: PLR0911, PLR0912
        match self:
            case Interval.Unison:
                return 0
            case Interval.MinorSecond:
                return 1
            case Interval.MajorSecond:
                return 2
            case Interval.MinorThird:
                return 3
            case Interval.MajorThird:
                return 4
            case Interval.PerfectFourth:
                return 5
            case Interval.Tritone:
                return 6
            case Interval.PerfectFifth:
                return 7
            case Interval.MinorSixth:
                return 8
            case Interval.MajorSixth:
                return 9
            case Interval.MinorSeventh:
                return 10
            case Interval.MajorSeventh:
                return 11
            case Interval.Octave:
                return 12
            case Interval.MinorNinth:
                return 13
            case Interval.MajorNinth:
                return 14
            case Interval.MinorTenth:
                return 15
            case Interval.MajorTenth:
                return 16
            case Interval.PerfectEleventh:
                return 17
            case Interval.AugmentedEleventh:
                return 18
            case Interval.PerfectTwelfth:
                return 19
            case Interval.MinorThirteenth:
                return 20
            case Interval.MajorThirteenth:
                return 21

    @classmethod
    def from_int(cls, interval_int: int) -> "Interval":
        mapping = {
            0: cls.Unison,
            1: cls.MinorSecond,
            2: cls.MajorSecond,
            3: cls.MinorThird,
            4: cls.MajorThird,
            5: cls.PerfectFourth,
            6: cls.Tritone,
            7: cls.PerfectFifth,
            8: cls.MinorSixth,
            9: cls.MajorSixth,
            10: cls.MinorSeventh,
            11: cls.MajorSeventh,
            12: cls.Octave,
            13: cls.MinorNinth,
            14: cls.MajorNinth,
            15: cls.MinorTenth,
            16: cls.MajorTenth,
            17: cls.PerfectEleventh,
            18: cls.AugmentedEleventh,
            19: cls.PerfectTwelfth,
            20: cls.MinorThirteenth,
            21: cls.MajorThirteenth,
        }
        if interval_int not in mapping:
            msg = f"Invalid interval: {interval_int}"
            raise ParseError(msg)
        return mapping[interval_int]

    def __str__(self) -> str:
        return self.to_str()

    def __repr__(self) -> str:
        return self.value
