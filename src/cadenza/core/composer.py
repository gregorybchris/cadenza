import logging
import math
from dataclasses import dataclass

from cadenza.core.constants import N_NOTES
from cadenza.core.note import Note
from cadenza.core.pitch import Pitch
from cadenza.core.transposer import Transposer
from cadenza.core.voicing import Voicing

logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class Composer:
    @classmethod
    def frequency_to_pitch(cls, frequency: float) -> Pitch:
        lowest_pitch = Pitch(note=Note.new_c(), octave=1)
        # NOTE: Offset slightly to allow for rounding errors
        lowest_pitch_frequency = cls.pitch_to_frequency(lowest_pitch) - 0.1
        if frequency < lowest_pitch_frequency:
            msg = f"Frequency {frequency} is lower than lowest allowed frequency {lowest_pitch_frequency}"
            raise ValueError(msg)

        n_semitones = round(N_NOTES * (math.log2(frequency) - math.log2(Pitch.REFERENCE_FREQUENCY)))
        n_octaves = n_semitones // N_NOTES
        n_degrees = n_semitones % N_NOTES
        # NOTE: This unsafe call is inevitable because we have no key information from a frequency.
        note = Note.from_integer_unsafe(Pitch.REFERENCE_NOTE.to_integer() + n_degrees)
        octave = Pitch.REFERENCE_OCTAVE + n_octaves
        return Pitch(note=note, octave=octave)

    @classmethod
    def pitch_to_frequency(cls, pitch: Pitch) -> float:
        degree_difference = pitch.note.to_integer() - Pitch.REFERENCE_NOTE.to_integer()
        octave_difference = pitch.octave - Pitch.REFERENCE_OCTAVE
        n_semitones = degree_difference + octave_difference * N_NOTES
        return Pitch.REFERENCE_FREQUENCY * 2 ** (n_semitones / N_NOTES)

    @classmethod
    def _get_left_hand_pitch(cls, voicing: Voicing) -> Pitch:
        # NOTE: The left hand plays the bass note as written. Deriving it from its interval above
        # the root instead would respell it, turning the G of D♭/G into an A♭♭.
        note = voicing.chord.bass or voicing.chord.root
        octave = voicing.octave - 2
        if note.to_integer() < voicing.chord.root.to_integer():
            # NOTE: The bass sits below the root, so it belongs to the octave the root started in.
            octave += 1
        return Pitch(note=note, octave=octave)

    @classmethod
    def _apply_inversion(cls, voicing: Voicing, pitches: list[Pitch]) -> list[Pitch]:
        inversion_number = voicing.inversion.to_number()
        n_notes = len(pitches)
        if inversion_number >= n_notes:
            msg = f"The {voicing.inversion.to_written()} does not exist for a voicing with {n_notes} right hand notes."
            raise ValueError(msg)

        for _ in range(inversion_number):
            pitches[0].octave += 1
            pitches = [*pitches[1:], pitches[0]]
        return pitches

    @classmethod
    def voicing_to_pitches(cls, voicing: Voicing) -> list[Pitch]:
        lh_pitches: list[Pitch] = []
        if voicing.include_left_hand:
            lh_pitches = [cls._get_left_hand_pitch(voicing)]

        rh_intervals = voicing.chord.get_intervals()
        rh_root_pitch = Pitch(note=voicing.chord.root, octave=voicing.octave)
        rh_pitches = [Transposer.transpose_pitch_unsafe(rh_root_pitch, x.to_int()) for x in rh_intervals]
        rh_pitches = cls._apply_inversion(voicing, rh_pitches)

        return lh_pitches + rh_pitches
