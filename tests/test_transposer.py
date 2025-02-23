import logging

from cadenza import DiatonicScale, Note, Pitch, Transposer

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
