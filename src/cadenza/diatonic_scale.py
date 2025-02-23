import logging
from typing import Iterator, Self

from pydantic import BaseModel

from cadenza.constants import N_DIATONIC_SCALE_NOTES, N_NOTES
from cadenza.diatonic_mode import DiatonicMode
from cadenza.note import Note
from cadenza.note_letter import NoteLetter

logger = logging.getLogger(__name__)


class DiatonicScale(BaseModel):
    root: Note
    mode: DiatonicMode

    @classmethod
    def major(cls, root: Note) -> Self:
        return cls(root=root, mode=DiatonicMode.Ionian)

    @classmethod
    def minor(cls, root: Note) -> Self:
        return cls(root=root, mode=DiatonicMode.Aeolian)

    def get_notes(self) -> list[Note]:
        return list(self.iter_notes())

    def iter_notes(self) -> Iterator[Note]:
        prev_note = self.root
        for step_size in self.mode.get_semitone_sequence():
            yield prev_note
            next_letter_index = (prev_note.letter.to_index() + 1) % N_DIATONIC_SCALE_NOTES
            next_letter = NoteLetter.from_index(next_letter_index)
            next_note_natural = Note(letter=next_letter)
            next_note_natural_integer = next_note_natural.to_integer()
            next_note_integer = (prev_note.to_integer() + step_size) % N_NOTES
            semitone_distance = next_note_natural_integer - next_note_integer
            n_sharps = abs(min(0, semitone_distance))
            n_flats = abs(max(0, semitone_distance))
            next_note = Note(letter=next_letter, n_sharps=n_sharps, n_flats=n_flats)
            prev_note = next_note
