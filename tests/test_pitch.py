import math

from cadenza import Note, Pitch


class TestPitch:
    def test_add_basic(self) -> None:
        pitch_a = Pitch(note=Note.C, octave=4)
        pitch_b = pitch_a + 1
        assert pitch_b.note == Note.CSharp
        assert pitch_b.octave == 4

    def test_add_across_octaves(self) -> None:
        pitch_a = Pitch(note=Note.G, octave=3)
        pitch_b = pitch_a + 6
        assert pitch_b.note == Note.CSharp
        assert pitch_b.octave == 4

    def test_add_with_flat(self) -> None:
        pitch_a = Pitch(note=Note.DFlat, octave=4)
        pitch_b = pitch_a + 5
        assert pitch_b.note == Note.GFlat
        assert pitch_b.octave == 4

    def test_to_frequency_concert_a(self) -> None:
        middle_c = Pitch(note=Note.C, octave=4)
        concert_a = middle_c + 9
        assert math.isclose(concert_a.to_frequency(), 440.0, rel_tol=1e-3)

    def test_from_frequency(self) -> None:
        concert_a_frequency = 440.0
        concert_a_pitch = Pitch.from_frequency(concert_a_frequency)
        assert concert_a_pitch.note == Note.A
        assert concert_a_pitch.octave == 4

        low_c_frequency = 32.7
        low_c_pitch = Pitch.from_frequency(low_c_frequency)
        assert low_c_pitch.note == Note.C
        assert low_c_pitch.octave == 1
