import logging
from enum import StrEnum
from typing import Any

from cadenza.utils.symbol_utils import add_symbols, remove_symbols

logger = logging.getLogger(__name__)


class Note(StrEnum):
    A = "A"
    A_SHARP = "A#"
    B_FLAT = "Bb"
    B = "B"
    C = "C"
    C_SHARP = "C#"
    D_FLAT = "Db"
    D = "D"
    D_SHARP = "D#"
    E_FLAT = "Eb"
    E = "E"
    F = "F"
    F_SHARP = "F#"
    G_FLAT = "Gb"
    G = "G"
    G_SHARP = "G#"
    A_FLAT = "Ab"

    @classmethod
    def from_str(cls, note_str: str) -> "Note":
        return cls(remove_symbols(note_str))

    def to_str(self, symbols: bool = True) -> str:
        if symbols:
            return add_symbols(self.value)
        return self.value

    def __add__(self, other: Any) -> "Note":
        if not isinstance(other, int):
            msg = f"Invalid type for addition: {type(other)}"
            raise ValueError(msg)
        notes = list(Note)
        return Note(notes[(notes.index(self) + other) % len(notes)])

    def __sub__(self, other: Any) -> "Note":
        if not isinstance(other, int):
            msg = f"Invalid type for subtraction: {type(other)}"
            raise ValueError(msg)
        notes = list(Note)
        return Note(notes[(notes.index(self) - other) % len(notes)])

    def __str__(self) -> str:
        return self.to_str()

    def __repr__(self) -> str:
        return self.value
