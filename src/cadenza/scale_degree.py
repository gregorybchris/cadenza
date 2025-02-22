import logging
from enum import StrEnum, auto
from typing import Self

from cadenza.interval import Interval

logger = logging.getLogger(__name__)


class ScaleDegree(StrEnum):
    Tonic = auto()
    Supertonic = auto()
    Mediant = auto()
    Subdominant = auto()
    Dominant = auto()
    Submediant = auto()
    LeadingTone = auto()

    def to_written(self) -> str:  # noqa: PLR0911
        match self:
            case ScaleDegree.Tonic:
                return "tonic"
            case ScaleDegree.Supertonic:
                return "supertonic"
            case ScaleDegree.Mediant:
                return "mediant"
            case ScaleDegree.Subdominant:
                return "subdominant"
            case ScaleDegree.Dominant:
                return "dominant"
            case ScaleDegree.Submediant:
                return "submediant"
            case ScaleDegree.LeadingTone:
                return "leading tone"

    def to_symbol(self) -> str:  # noqa: PLR0911
        match self:
            case ScaleDegree.Tonic:
                return "I"
            case ScaleDegree.Supertonic:
                return "II"
            case ScaleDegree.Mediant:
                return "III"
            case ScaleDegree.Subdominant:
                return "IV"
            case ScaleDegree.Dominant:
                return "V"
            case ScaleDegree.Submediant:
                return "VI"
            case ScaleDegree.LeadingTone:
                return "VII"

    @classmethod
    def from_int(cls, degree: int) -> "ScaleDegree":
        degree = degree % 8
        return {
            1: cls.Tonic,
            2: cls.Supertonic,
            3: cls.Mediant,
            4: cls.Subdominant,
            5: cls.Dominant,
            6: cls.Submediant,
            7: cls.LeadingTone,
        }[degree]

    def to_int(self) -> int:  # noqa: PLR0911
        match self:
            case ScaleDegree.Tonic:
                return 1
            case ScaleDegree.Supertonic:
                return 2
            case ScaleDegree.Mediant:
                return 3
            case ScaleDegree.Subdominant:
                return 4
            case ScaleDegree.Dominant:
                return 5
            case ScaleDegree.Submediant:
                return 6
            case ScaleDegree.LeadingTone:
                return 7

    @classmethod
    def from_interval(cls, interval: Interval) -> "ScaleDegree":  # noqa: PLR0911, PLR0912
        match interval:
            case Interval.Unison:
                return cls.Tonic
            case Interval.MinorSecond:
                msg = "Minor second is not a valid interval for scale degrees"
                raise ValueError(msg)
            case Interval.MajorSecond:
                return cls.Supertonic
            case Interval.MinorThird:
                return cls.Mediant
            case Interval.MajorThird:
                return cls.Mediant
            case Interval.PerfectFourth:
                return cls.Subdominant
            case Interval.Tritone:
                msg = "Tritone is not a valid interval for scale degrees"
                raise ValueError(msg)
            case Interval.PerfectFifth:
                return cls.Dominant
            case Interval.MinorSixth:
                return cls.Submediant
            case Interval.MajorSixth:
                return cls.Submediant
            case Interval.MinorSeventh:
                return cls.LeadingTone
            case Interval.MajorSeventh:
                return cls.LeadingTone
            case Interval.Octave:
                return cls.Tonic
            case Interval.MinorNinth:
                msg = "Minor ninth is not a valid interval for scale degrees"
                raise ValueError(msg)
            case Interval.MajorNinth:
                msg = "Major ninth is not a valid interval for scale degrees"
                raise ValueError(msg)
            case Interval.MinorTenth:
                msg = "Minor tenth is not a valid interval for scale degrees"
                raise ValueError(msg)
            case Interval.MajorTenth:
                msg = "Major tenth is not a valid interval for scale degrees"
                raise ValueError(msg)
            case Interval.PerfectEleventh:
                msg = "Perfect eleventh is not a valid interval for scale degrees"
                raise ValueError(msg)
            case Interval.AugmentedEleventh:
                msg = "Augmented eleventh is not a valid interval for scale degrees"
                raise ValueError(msg)
            case Interval.PerfectTwelfth:
                msg = "Perfect twelfth is not a valid interval for scale degrees"
                raise ValueError(msg)
            case Interval.MinorThirteenth:
                msg = "Minor thirteenth is not a valid interval for scale degrees"
                raise ValueError(msg)
            case Interval.MajorThirteenth:
                msg = "Major thirteenth is not a valid interval for scale degrees"
                raise ValueError(msg)

    @classmethod
    def from_str(cls, scale_degree_str: str) -> Self:
        return cls[scale_degree_str]

    def __str__(self) -> str:
        return self.to_written()

    def __repr__(self) -> str:
        return self.value
