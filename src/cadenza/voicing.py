import logging
from typing import Self

from pydantic import BaseModel

from cadenza.chord import Chord
from cadenza.inversion import Inversion

logger = logging.getLogger(__name__)


class Voicing(BaseModel):
    chord: Chord
    inversion: Inversion
    octave: int
    include_left_hand: bool = True

    @classmethod
    def from_chord(cls, chord: Chord, inversion: Inversion, octave: int, include_left_hand: bool = True) -> Self:
        return cls(chord=chord, inversion=inversion, octave=octave, include_left_hand=include_left_hand)
