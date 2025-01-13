import logging
from enum import StrEnum, auto

logger = logging.getLogger(__name__)


class Interval(StrEnum):
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

    def to_written(self) -> str:  # noqa: PLR0911
        match self:
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

    @classmethod
    def from_str(cls, interval_str: str) -> "Interval":  # noqa: PLR0911
        match interval_str:
            case "m2":
                return cls.MinorSecond
            case "M2":
                return cls.MajorSecond
            case "m3":
                return cls.MinorThird
            case "M3":
                return cls.MajorThird
            case "P4":
                return cls.PerfectFourth
            case "TT":
                return cls.Tritone
            case "P5":
                return cls.PerfectFifth
            case "m6":
                return cls.MinorSixth
            case "M6":
                return cls.MajorSixth
            case "m7":
                return cls.MinorSeventh
            case "M7":
                return cls.MajorSeventh
            case "P8":
                return cls.Octave

        msg = f"Invalid interval: {interval_str}"
        raise ValueError(msg)

    def to_str(self) -> str:  # noqa: PLR0911
        match self:
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

    def __str__(self) -> str:
        return self.to_str()

    def __repr__(self) -> str:
        return self.value
