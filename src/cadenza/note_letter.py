import logging
from enum import StrEnum
from typing import Self

from cadenza.constants import N_DIATONIC_SCALE_NOTES

logger = logging.getLogger(__name__)


class NoteLetter(StrEnum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"

    def to_index(self) -> int:
        mapping = {
            NoteLetter.C: 0,
            NoteLetter.D: 1,
            NoteLetter.E: 2,
            NoteLetter.F: 3,
            NoteLetter.G: 4,
            NoteLetter.A: 5,
            NoteLetter.B: 6,
        }
        return mapping[self]

    @classmethod
    def from_index(cls, index: int) -> "NoteLetter":
        index %= N_DIATONIC_SCALE_NOTES
        mapping = {
            0: NoteLetter.C,
            1: NoteLetter.D,
            2: NoteLetter.E,
            3: NoteLetter.F,
            4: NoteLetter.G,
            5: NoteLetter.A,
            6: NoteLetter.B,
        }
        return mapping[index]

    @classmethod
    def from_str(cls, note_letter_str: str) -> Self:
        return cls(note_letter_str)

    def to_str(self) -> str:
        return self.value

    def __str__(self) -> str:
        return self.to_str()

    def __repr__(self) -> str:
        return self.value
