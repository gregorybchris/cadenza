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
        note = self.root
        for step_size in self.mode.get_semitone_sequence():
            yield note

            # Ensure next note has a different letter
            next_letter_index = (note.letter.to_index() + 1) % N_DIATONIC_SCALE_NOTES
            next_letter = NoteLetter.from_index(next_letter_index)
            next_note_natural = Note(letter=next_letter)
            next_note_natural_integer = next_note_natural.to_integer()
            next_note_integer = (note.to_integer() + step_size) % N_NOTES

            # Calculate number of accidentals, taking into account wrap around
            semitone_diff = next_note_integer - next_note_natural_integer
            if abs(semitone_diff) > N_NOTES / 2:
                semitone_diff = (N_NOTES - semitone_diff) * (-1 if semitone_diff > 0 else 1)
            n_sharps = abs(max(0, semitone_diff))
            n_flats = abs(min(0, semitone_diff))

            next_note = Note(letter=next_letter, n_sharps=n_sharps, n_flats=n_flats)
            note = next_note

    def iter_key_signature(self) -> Iterator[Note]:
        # TODO: Sort key signature using circle of fifths
        for note in self.iter_notes():
            if note.n_sharps > 1 or note.n_flats > 1:
                accidental_str = "sharp" if note.n_sharps > 1 else "flat"
                msg = (
                    f"The diatonic scale {self.root.to_str()} {self.mode.to_written()}"
                    f" has a double {accidental_str} and does not have a standard key signature."
                )
                raise ValueError(msg)

            if note.n_sharps > 0 or note.n_flats > 0:
                yield note

    def get_key_signature(self) -> list[Note]:
        return list(self.iter_key_signature())
