import logging
import math
from typing import Any, ClassVar, Self

from pydantic import BaseModel

from cadenza.note import Note

logger = logging.getLogger(__name__)


class Pitch(BaseModel):
    # NOTE: We start at C because the octave numbers typically change at C
    # A4 (concert A) = 440.0 Hz
    # C4 (middle C) = 261.63 Hz
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

    @classmethod
    def from_frequency(cls, frequency: float) -> Self:
        lowest_pitch = cls(note=Note.C, octave=1)
        lowest_pitch_frequency = lowest_pitch.to_frequency() - 0.1  # Offset slightly to allow for rounding errors
        if frequency < lowest_pitch_frequency:
            msg = f"Frequency {frequency} is lower than lowest allowed frequency {lowest_pitch_frequency}"
            raise ValueError(msg)

        n_semitones = round(12 * (math.log2(frequency) - math.log2(cls.REFERENCE_FREQUENCY)))
        n_octaves = n_semitones // 12
        n_degrees = n_semitones % 12
        note = cls.REFERENCE_NOTE + n_degrees
        octave = cls.REFERENCE_OCTAVE + n_octaves
        return cls(note=note, octave=octave)

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
