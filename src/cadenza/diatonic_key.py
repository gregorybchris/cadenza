from pydantic import BaseModel

from cadenza.diatonic_mode import DiatonicMode
from cadenza.note import Note


class DiatonicKey(BaseModel):
    root: Note
    mode: DiatonicMode
