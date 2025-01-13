import logging
from enum import StrEnum, auto
from typing import Self

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
    def from_str(cls, mode_str: str) -> Self:
        return cls[mode_str]

    def __str__(self) -> str:
        return self.to_written()

    def __repr__(self) -> str:
        return self.value
