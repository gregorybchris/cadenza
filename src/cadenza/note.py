import logging
from enum import StrEnum
from typing import Any, Self

from cadenza.accidental import Accidental
from cadenza.constants import N_NOTES
from cadenza.utils.symbol_utils import add_symbols, remove_symbols

logger = logging.getLogger(__name__)


class Note(StrEnum):
    A = "A"
    ASharp = "A#"
    BFlat = "Bb"
    B = "B"
    C = "C"
    CSharp = "C#"
    DFlat = "Db"
    D = "D"
    DSharp = "D#"
    EFlat = "Eb"
    E = "E"
    F = "F"
    FSharp = "F#"
    GFlat = "Gb"
    G = "G"
    GSharp = "G#"
    AFlat = "Ab"

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
            Note.BFlat: Note.ASharp,
            Note.EFlat: Note.DSharp,
            Note.AFlat: Note.GSharp,
            Note.DFlat: Note.CSharp,
            Note.GFlat: Note.FSharp,
        }
        if self in mapping:
            return mapping[self]
        return self

    def as_flat(self) -> "Note":
        mapping = {
            Note.ASharp: Note.BFlat,
            Note.DSharp: Note.EFlat,
            Note.GSharp: Note.AFlat,
            Note.CSharp: Note.DFlat,
            Note.FSharp: Note.GFlat,
        }
        if self in mapping:
            return mapping[self]
        return self

    def to_index(self) -> int:
        mapping = {
            Note.C: 0,
            Note.CSharp: 1,
            Note.DFlat: 1,
            Note.D: 2,
            Note.DSharp: 3,
            Note.EFlat: 3,
            Note.E: 4,
            Note.F: 5,
            Note.FSharp: 6,
            Note.GFlat: 6,
            Note.G: 7,
            Note.GSharp: 8,
            Note.AFlat: 8,
            Note.A: 9,
            Note.ASharp: 10,
            Note.BFlat: 10,
            Note.B: 11,
        }
        return mapping[self]

    @classmethod
    def from_index(cls, index: int, accidental: Accidental = Accidental.Sharp) -> "Note":
        mapping = {
            0: Note.C,
            1: Note.CSharp if accidental == Accidental.Sharp else Note.DFlat,
            2: Note.D,
            3: Note.DSharp if accidental == Accidental.Sharp else Note.EFlat,
            4: Note.E,
            5: Note.F,
            6: Note.FSharp if accidental == Accidental.Sharp else Note.GFlat,
            7: Note.G,
            8: Note.GSharp if accidental == Accidental.Sharp else Note.AFlat,
            9: Note.A,
            10: Note.ASharp if accidental == Accidental.Sharp else Note.BFlat,
            11: Note.B,
        }
        return mapping[index]

    def add(self, semitones: int, accidental: Accidental) -> "Note":
        new_index = (self.to_index() + semitones) % N_NOTES
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
