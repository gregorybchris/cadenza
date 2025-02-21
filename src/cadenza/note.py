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
            Note.C: 0,
            Note.C_SHARP: 1,
            Note.D_FLAT: 1,
            Note.D: 2,
            Note.D_SHARP: 3,
            Note.E_FLAT: 3,
            Note.E: 4,
            Note.F: 5,
            Note.F_SHARP: 6,
            Note.G_FLAT: 6,
            Note.G: 7,
            Note.G_SHARP: 8,
            Note.A_FLAT: 8,
            Note.A: 9,
            Note.A_SHARP: 10,
            Note.B_FLAT: 10,
            Note.B: 11,
        }
        return mapping[self]

    @classmethod
    def from_index(cls, index: int, accidental: Accidental = Accidental.Sharp) -> "Note":
        mapping = {
            0: Note.C,
            1: Note.C_SHARP if accidental == Accidental.Sharp else Note.D_FLAT,
            2: Note.D,
            3: Note.D_SHARP if accidental == Accidental.Sharp else Note.E_FLAT,
            4: Note.E,
            5: Note.F,
            6: Note.F_SHARP if accidental == Accidental.Sharp else Note.G_FLAT,
            7: Note.G,
            8: Note.G_SHARP if accidental == Accidental.Sharp else Note.A_FLAT,
            9: Note.A,
            10: Note.A_SHARP if accidental == Accidental.Sharp else Note.B_FLAT,
            11: Note.B,
        }
        return mapping[index]

    def add(self, semitones: int, accidental: Accidental) -> "Note":
        new_index = (self.to_index() + semitones) % 12
        return Note.from_index(new_index, accidental)

    def __add__(self, semitones: Any) -> "Note":
        if not isinstance(semitones, int):
            msg = f"Cannot add type with Note: {type(semitones)}"
            raise ValueError(msg)
        accidental = Accidental.Flat if self.is_flat() else Accidental.Sharp
        return self.add(semitones, accidental)

    def __sub__(self, semitones: Any) -> "Note":
        if not isinstance(semitones, int):
            msg = f"Cannot subtract type with Note: {type(semitones)}"
            raise ValueError(msg)
        accidental = Accidental.Flat if self.is_flat() else Accidental.Sharp
        return self.add(-semitones, accidental)

    def __str__(self) -> str:
        return self.to_str()

    def __repr__(self) -> str:
        return self.value
