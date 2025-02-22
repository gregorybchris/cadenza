import logging

from pydantic import BaseModel

from cadenza.diatonic_mode import DiatonicMode
from cadenza.note import Note

logger = logging.getLogger(__name__)


class DiatonicScale(BaseModel):
    root: Note
    mode: DiatonicMode

    def get_notes(self) -> list[Note]:
        # TODO: Use .add() and pass the correct accidental
        return [self.root + interval.to_int() for interval in self.mode.get_intervals()]

    def get_key_signature(self) -> list[Note]:
        raise NotImplementedError


# [Bb] = F major / D minor
# [Bb, Eb] = Bb major / G minor
# [Bb, Eb, Ab] = Eb major / C minor
# [Bb, Eb, Ab, Db] = Ab major / F minor
# [Bb, Eb, Ab, Db, Gb] = Db major / Bb minor
# [Bb, Eb, Ab, Db, Gb, Cb] = Gb major / Gb minor
# [Bb, Eb, Ab, Db, Gb, Cb, Fb] = Cb major / Ab minor

# [F#] = G major / E minor
# [F#, C#] = D major / B minor
# [F#, C#, G#] = A major / F# minor
# [F#, C#, G#, D#] = E major / C# minor
# [F#, C#, G#, D#, A#] = B major / G# minor
# [F#, C#, G#, D#, A#, E#] = F# major / D# minor
# [F#, C#, G#, D#, A#, E#, B#] = C# major / A# minor
