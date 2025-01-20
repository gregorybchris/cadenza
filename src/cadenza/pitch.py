import logging
from typing import ClassVar

from pydantic import BaseModel

from cadenza.note import Note

logger = logging.getLogger(__name__)


class Pitch(BaseModel):
    # TODO: Update this so that the octaves start on C and not A
    # Middle C (C4) is 3 semitones above A3, which is 220 Hz
    # A4 is 440 Hz, so C4 is 261.63 Hz
    REFERENCE_OCTAVE: ClassVar[int] = 4
    REFERENCE_FREQUENCY: ClassVar[float] = 440.0
    REFERENCE_NOTE: ClassVar[Note] = Note.A

    note: Note
    octave: int

    def get_frequency(self) -> float:
        degree_difference = self.note.to_index() - self.REFERENCE_NOTE.to_index()
        octave_difference = self.octave - self.REFERENCE_OCTAVE
        n_semitones = degree_difference + octave_difference * 12
        return self.REFERENCE_FREQUENCY * 2 ** (n_semitones / 12)
