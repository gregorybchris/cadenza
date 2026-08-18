import logging
from typing import Iterator, Self

from pydantic import BaseModel

from cadenza.core.constants import N_DIATONIC_SCALE_NOTES, N_NOTES
from cadenza.core.diatonic_mode import DiatonicMode
from cadenza.core.note import Note
from cadenza.core.note_letter import NoteLetter

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
            note = Note.from_letter_and_pitch_class(next_letter, (note.to_integer() + step_size) % N_NOTES)

    def iter_key_signature(self) -> Iterator[Note]:
        notes = []
        for note in self.iter_notes():
            if note.n_sharps > 1 or note.n_flats > 1:
                accidental_str = "sharp" if note.n_sharps > 1 else "flat"
                msg = (
                    f"The diatonic scale {self.root.to_str()} {self.mode.to_written()}"
                    f" has a double {accidental_str} and does not have a standard key signature."
                )
                raise ValueError(msg)

            if note.n_sharps > 0 or note.n_flats > 0:
                notes.append(note)

        # NOTE: The order of the sharps/flats can be determined quickly from the circle of fifths,
        # but hardcoding the order is simpler. They can also be derived by enumerating the number of
        # accidentals in all scales and sorting them by the number of accidentals.
        sharp_notes_order = [
            Note.new_f_sharp(),
            Note.new_c_sharp(),
            Note.new_g_sharp(),
            Note.new_d_sharp(),
            Note.new_a_sharp(),
            Note.new_e_sharp(),
            Note.new_b_sharp(),
        ]
        flat_notes_order = [
            Note.new_b_flat(),
            Note.new_e_flat(),
            Note.new_a_flat(),
            Note.new_d_flat(),
            Note.new_g_flat(),
            Note.new_c_flat(),
            Note.new_f_flat(),
        ]

        for note in sharp_notes_order:
            if note in notes:
                yield note
        for note in flat_notes_order:
            if note in notes:
                yield note

    def get_key_signature(self) -> list[Note]:
        return list(self.iter_key_signature())
