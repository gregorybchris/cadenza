import logging
from typing import ClassVar

from pydantic import BaseModel

from cadenza.note import Note

logger = logging.getLogger(__name__)


class Pitch(BaseModel):
    # NOTE: We start at C because the octave numbers typically change at C
    # A4 (concert A) = 440.0 Hz
    # C4 (middle C) = 261.63 Hz
    REFERENCE_OCTAVE: ClassVar[int] = 4
    REFERENCE_FREQUENCY: ClassVar[float] = 261.63
    REFERENCE_NOTE: ClassVar[Note] = Note.new_c()

    note: Note
    octave: int

    def __str__(self) -> str:
        return f"{self.note.to_str()}{self.octave}"

    def __repr__(self) -> str:
        return f"{self.note.to_str()}{self.octave}"
