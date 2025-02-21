from cadenza import Note, Pitch


class TestPitch:
    def test_add_basic(self) -> None:
        pitch_a = Pitch(note=Note.C, octave=4)
        pitch_b = pitch_a + 1
        assert pitch_b.note == Note.C_SHARP
        assert pitch_b.octave == 4

    def test_add_across_octaves(self) -> None:
        pitch_a = Pitch(note=Note.G, octave=3)
        pitch_b = pitch_a + 6
        assert pitch_b.note == Note.C_SHARP
        assert pitch_b.octave == 4

    def test_add_with_flat(self) -> None:
        pitch_a = Pitch(note=Note.D_FLAT, octave=4)
        pitch_b = pitch_a + 5
        assert pitch_b.note == Note.G_FLAT
        assert pitch_b.octave == 4
