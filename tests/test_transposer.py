import logging

from cadenza import Chord, DiatonicScale, Note, Pitch, Quality, Transposer

logger = logging.getLogger(__name__)


class TestTransposer:
    def test_transpose_unsafe_basic(self) -> None:
        pitch_1 = Pitch(note=Note.new_c(), octave=4)
        pitch_2 = Transposer.transpose_pitch_unsafe(pitch_1, 1)
        assert pitch_2.note == Note.new_d_flat()
        assert pitch_2.octave == 4

    def test_transpose_unsafe_across_octaves(self) -> None:
        pitch_1 = Pitch(note=Note.new_g(), octave=3)
        pitch_2 = Transposer.transpose_pitch_unsafe(pitch_1, 6)
        assert pitch_2.note == Note.new_d_flat()
        assert pitch_2.octave == 4

    def test_transpose_pitch_with_flat(self) -> None:
        pitch_1 = Pitch(note=Note.new_a_flat(), octave=4)
        scale = DiatonicScale.major(Note.new_a_flat())
        pitch_2 = Transposer.transpose_pitch(pitch_1, 7, scale=scale)
        assert pitch_2.note == Note.new_e_flat()
        assert pitch_2.octave == 5

    def test_transpose_power_chord_preserves_quality(self) -> None:
        chord = Chord.from_str("A5/E")
        scale = DiatonicScale.major(Note.new_c())
        transposed = Transposer.transpose_chord(chord, 3, scale=scale)
        assert transposed.quality == Quality.Power
        assert transposed.root == Note.new_c()
        assert transposed.bass == Note.new_g()
