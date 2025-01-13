import logging

from pydantic import BaseModel

from cadenza.chord import Chord
from cadenza.inversion import Inversion
from cadenza.pitch import Pitch

logger = logging.getLogger(__name__)


class Voicing(BaseModel):
    chord: Chord
    inversion: Inversion
    octave: int

    def get_pitches(self) -> list[Pitch]:
        notes = self.chord.get_notes()
        inversion_number = self.inversion.get_number()

        n_notes = len(notes)
        if inversion_number >= n_notes:
            msg = f"The {self.inversion.to_written()} does not exist for a voicing with {n_notes} notes."
            logger.error(msg)
            raise ValueError(msg)

        pitches = [Pitch(note=note, octave=self.octave) for note in notes]
        for _ in range(inversion_number):
            transposed_pitch = pitches[0]
            transposed_pitch.octave += 1
            pitches = pitches[1:] + [transposed_pitch]
        return pitches
