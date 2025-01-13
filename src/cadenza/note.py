import logging
from enum import StrEnum
from typing import Any, Self

from cadenza.accidental import Accidental
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
    def from_str(cls, note_str: str) -> Self:
        return cls(remove_symbols(note_str))

    def to_str(self, symbols: bool = True) -> str:
        if symbols:
            return add_symbols(self.value)
        return self.value

    def is_sharp(self) -> bool:
        return "#" in self.value

    def is_flat(self) -> bool:
        return "b" in self.value

    def as_sharp(self) -> "Note":
        mapping = {
            Note.B_FLAT: Note.A_SHARP,
            Note.E_FLAT: Note.D_SHARP,
            Note.A_FLAT: Note.G_SHARP,
            Note.D_FLAT: Note.C_SHARP,
            Note.G_FLAT: Note.F_SHARP,
        }
        if self in mapping:
            return mapping[self]
        return self

    def as_flat(self) -> "Note":
        mapping = {
            Note.A_SHARP: Note.B_FLAT,
            Note.D_SHARP: Note.E_FLAT,
            Note.G_SHARP: Note.A_FLAT,
            Note.C_SHARP: Note.D_FLAT,
            Note.F_SHARP: Note.G_FLAT,
        }
        if self in mapping:
            return mapping[self]
        return self

    def to_index(self) -> int:
        mapping = {
            Note.A: 0,
            Note.A_SHARP: 1,
            Note.B_FLAT: 1,
            Note.B: 2,
            Note.C: 3,
            Note.C_SHARP: 4,
            Note.D_FLAT: 4,
            Note.D: 5,
            Note.D_SHARP: 6,
            Note.E_FLAT: 6,
            Note.E: 7,
            Note.F: 8,
            Note.F_SHARP: 9,
            Note.G_FLAT: 9,
            Note.G: 10,
            Note.G_SHARP: 11,
            Note.A_FLAT: 11,
        }
        return mapping[self]

    @classmethod
    def from_index(cls, index: int, accidental: Accidental = Accidental.Sharp) -> "Note":
        mapping = {
            0: Note.A,
            1: Note.A_SHARP if accidental == Accidental.Sharp else Note.B_FLAT,
            2: Note.B,
            3: Note.C,
            4: Note.C_SHARP if accidental == Accidental.Sharp else Note.D_FLAT,
            5: Note.D,
            6: Note.D_SHARP if accidental == Accidental.Sharp else Note.E_FLAT,
            7: Note.E,
            8: Note.F,
            9: Note.F_SHARP if accidental == Accidental.Sharp else Note.G_FLAT,
            10: Note.G,
            11: Note.G_SHARP if accidental == Accidental.Sharp else Note.A_FLAT,
        }
        return mapping[index]

    def add(self, interval: int, accidental: Accidental) -> "Note":
        new_index = (self.to_index() + interval) % 12
        return Note.from_index(new_index, accidental)

    def __add__(self, other: Any) -> "Note":
        if not isinstance(other, int):
            msg = f"Cannot add type with Note: {type(other)}"
            raise ValueError(msg)
        accidental = Accidental.Flat if self.is_flat() else Accidental.Sharp
        return self.add(other, accidental)

    def __sub__(self, other: Any) -> "Note":
        if not isinstance(other, int):
            msg = f"Cannot subtract type with Note: {type(other)}"
            raise ValueError(msg)
        accidental = Accidental.Flat if self.is_flat() else Accidental.Sharp
        return self.add(-other, accidental)

    def __str__(self) -> str:
        return self.to_str()

    def __repr__(self) -> str:
        return self.value
