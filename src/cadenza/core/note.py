import logging
from typing import ClassVar, Optional, Self

from pydantic import BaseModel

from cadenza.core.constants import FLAT_CHAR, N_NOTES, SHARP_CHAR
from cadenza.core.note_letter import NoteLetter
from cadenza.utils.symbol_utils import add_symbols, remove_symbols

logger = logging.getLogger(__name__)


class Note(BaseModel):
    letter: NoteLetter
    n_sharps: int = 0
    n_flats: int = 0

    @classmethod
    def new_c(cls) -> "Note":
        return Note(letter=NoteLetter.C)

    @classmethod
    def new_c_sharp(cls) -> "Note":
        return Note(letter=NoteLetter.C, n_sharps=1)

    @classmethod
    def new_d_flat(cls) -> "Note":
        return Note(letter=NoteLetter.D, n_flats=1)

    @classmethod
    def new_d(cls) -> "Note":
        return Note(letter=NoteLetter.D)

    @classmethod
    def new_d_sharp(cls) -> "Note":
        return Note(letter=NoteLetter.D, n_sharps=1)

    @classmethod
    def new_e_flat(cls) -> "Note":
        return Note(letter=NoteLetter.E, n_flats=1)

    @classmethod
    def new_e(cls) -> "Note":
        return Note(letter=NoteLetter.E)

    @classmethod
    def new_e_sharp(cls) -> "Note":
        return Note(letter=NoteLetter.E, n_sharps=1)

    @classmethod
    def new_f_flat(cls) -> "Note":
        return Note(letter=NoteLetter.F, n_flats=1)

    @classmethod
    def new_f(cls) -> "Note":
        return Note(letter=NoteLetter.F)

    @classmethod
    def new_f_sharp(cls) -> "Note":
        return Note(letter=NoteLetter.F, n_sharps=1)

    @classmethod
    def new_g_flat(cls) -> "Note":
        return Note(letter=NoteLetter.G, n_flats=1)

    @classmethod
    def new_g(cls) -> "Note":
        return Note(letter=NoteLetter.G)

    @classmethod
    def new_g_sharp(cls) -> "Note":
        return Note(letter=NoteLetter.G, n_sharps=1)

    @classmethod
    def new_a_flat(cls) -> "Note":
        return Note(letter=NoteLetter.A, n_flats=1)

    @classmethod
    def new_a(cls) -> "Note":
        return Note(letter=NoteLetter.A)

    @classmethod
    def new_a_sharp(cls) -> "Note":
        return Note(letter=NoteLetter.A, n_sharps=1)

    @classmethod
    def new_b_flat(cls) -> "Note":
        return Note(letter=NoteLetter.B, n_flats=1)

    @classmethod
    def new_b(cls) -> "Note":
        return Note(letter=NoteLetter.B)

    @classmethod
    def new_b_sharp(cls) -> "Note":
        return Note(letter=NoteLetter.B, n_sharps=1)

    @classmethod
    def new_c_flat(cls) -> "Note":
        return Note(letter=NoteLetter.C, n_flats=1)

    @classmethod
    def from_str(cls, note_str: str) -> Self:
        note_str = remove_symbols(note_str)
        letter = NoteLetter.from_str(note_str[0])
        n_sharps = note_str.count(SHARP_CHAR)
        n_flats = note_str.count(FLAT_CHAR)
        return cls(letter=letter, n_sharps=n_sharps, n_flats=n_flats)

    def to_str(self, symbols: bool = True) -> str:
        ret = self.letter.to_str()
        ret += SHARP_CHAR * self.n_sharps
        ret += FLAT_CHAR * self.n_flats
        if symbols:
            ret = add_symbols(ret)
        return ret

    def to_integer(self) -> int:
        letter_mapping = {
            NoteLetter.C: 0,
            NoteLetter.D: 2,
            NoteLetter.E: 4,
            NoteLetter.F: 5,
            NoteLetter.G: 7,
            NoteLetter.A: 9,
            NoteLetter.B: 11,
        }
        return (letter_mapping[self.letter] + self.n_sharps - self.n_flats) % N_NOTES

    _NATURAL_LETTERS: ClassVar[dict[int, NoteLetter]] = {
        0: NoteLetter.C,
        2: NoteLetter.D,
        4: NoteLetter.E,
        5: NoteLetter.F,
        7: NoteLetter.G,
        9: NoteLetter.A,
        11: NoteLetter.B,
    }

    @classmethod
    def natural_from_integer(cls, index: int) -> Optional["Note"]:
        """The natural note with the given pitch class, or None where every spelling takes an accidental."""
        letter = cls._NATURAL_LETTERS.get(index % N_NOTES)
        return Note(letter=letter) if letter else None

    @classmethod
    def from_integer_unsafe(cls, index: int) -> "Note":
        # NOTE: This function is unsafe because it does not account for the key signature.
        # It will always return a note with a single flat or no accidentals. Prefer Speller
        # when the note has a tonic or a chord root to take its spelling from.
        natural = cls.natural_from_integer(index)
        if natural is not None:
            return natural
        return Note(letter=cls._NATURAL_LETTERS[(index + 1) % N_NOTES], n_flats=1)

    @classmethod
    def from_letter_and_pitch_class(cls, letter: NoteLetter, pitch_class: int) -> "Note":
        """The note with the given letter that sounds the given pitch class, with fewest accidentals."""
        difference = (pitch_class - Note(letter=letter).to_integer()) % N_NOTES
        if difference > N_NOTES / 2:
            difference -= N_NOTES
        return Note(letter=letter, n_sharps=max(0, difference), n_flats=abs(min(0, difference)))

    def is_enharmonic(self, other: "Note") -> bool:
        return self.to_integer() == other.to_integer()

    def __str__(self) -> str:
        return self.to_str()

    def __repr__(self) -> str:
        return self.to_str()
