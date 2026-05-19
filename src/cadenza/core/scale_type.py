import logging
from enum import StrEnum, auto
from typing import Self

logger = logging.getLogger(__name__)


class ScaleType(StrEnum):
    Major = auto()
    NaturalMinor = auto()

    def to_written(self) -> str:
        match self:
            case ScaleType.Major:
                return "major"
            case ScaleType.NaturalMinor:
                return "natural minor"

    @classmethod
    def from_str(cls, scale_str: str) -> Self:
        return cls[scale_str]

    def __str__(self) -> str:
        return self.to_written()

    def __repr__(self) -> str:
        return self.value
