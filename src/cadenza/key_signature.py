from pydantic import BaseModel

from cadenza.diatonic_mode import DiatonicMode
from cadenza.note import Note


class KeySignature(BaseModel):
    root: Note
    mode: DiatonicMode

    def get_accidentals(self) -> list[Note]:
        raise NotImplementedError
