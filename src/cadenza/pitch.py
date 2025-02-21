import logging
from typing import Any, ClassVar

from pydantic import BaseModel

from cadenza.note import Note

logger = logging.getLogger(__name__)


class Pitch(BaseModel):
    # Middle C (C4) is 3 semitones above A3 (220 Hz)
    # A4 is 440 Hz and C4 is 261.63 Hz
    REFERENCE_OCTAVE: ClassVar[int] = 4
    REFERENCE_FREQUENCY: ClassVar[float] = 261.63
    REFERENCE_NOTE: ClassVar[Note] = Note.C

    note: Note
    octave: int

    def to_frequency(self) -> float:
        degree_difference = self.note.to_index() - self.REFERENCE_NOTE.to_index()
        octave_difference = self.octave - self.REFERENCE_OCTAVE
        n_semitones = degree_difference + octave_difference * 12
        return self.REFERENCE_FREQUENCY * 2 ** (n_semitones / 12)

    def add(self, semitones: int) -> "Pitch":
        new_note = self.note + semitones
        new_octave = self.octave + (self.note.to_index() + semitones) // 12
        return Pitch(note=new_note, octave=new_octave)

    def __add__(self, semitones: Any) -> "Pitch":
        if not isinstance(semitones, int):
            msg = f"Cannot add type with Pitch: {type(semitones)}"
            raise ValueError(msg)
        return self.add(semitones)

    def __sub__(self, semitones: Any) -> "Pitch":
        if not isinstance(semitones, int):
            msg = f"Cannot subtract type with Pitch: {type(semitones)}"
            raise ValueError(msg)
        return self.add(-semitones)

    def __str__(self) -> str:
        return f"{self.note.value}{self.octave}"

    def __repr__(self) -> str:
        return f"{self.note.value}{self.octave}"
