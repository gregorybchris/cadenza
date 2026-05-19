from pydantic import BaseModel

from cadenza.core.diatonic_mode import DiatonicMode
from cadenza.core.note import Note


class DiatonicKey(BaseModel):
    root: Note
    mode: DiatonicMode
