import logging
from enum import StrEnum, auto
from typing import Self

logger = logging.getLogger(__name__)


class DiatonicMode(StrEnum):
    Ionian = auto()  # Major
    Dorian = auto()
    Phrygian = auto()
    Lydian = auto()
    Mixolydian = auto()
    Aeolian = auto()  # Natural Minor
    Locrian = auto()

    def to_written(self) -> str:
        return self.value

    @classmethod
    def from_str(cls, mode_str: str) -> Self:
        return cls[mode_str]

    def __str__(self) -> str:
        return self.to_written()

    def __repr__(self) -> str:
        return self.value
