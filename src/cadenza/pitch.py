import logging

from pydantic import BaseModel

from cadenza.note import Note

logger = logging.getLogger(__name__)


class Pitch(BaseModel):
    note: Note
    octave: int
