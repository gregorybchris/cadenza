import pytest

from cadenza import Chord
from cadenza.extension import Extension
from cadenza.inversion import Inversion
from cadenza.note import Note
from cadenza.pitch import Pitch
from cadenza.quality import Quality
from cadenza.voicing import Voicing


class TestVoicing:
    def test_get_pitches_root(self) -> None:
        chord = Chord(root=Note.new_c(), quality=Quality.Major)
        voicing = Voicing(chord=chord, inversion=Inversion.Root, octave=4)
        pitches = voicing.to_pitches()
        assert pitches == [
            Pitch(note=Note.new_c(), octave=2),
            Pitch(note=Note.new_c(), octave=4),
            Pitch(note=Note.new_e(), octave=4),
            Pitch(note=Note.new_g(), octave=4),
        ]

    def test_get_pitches_first_inversion(self) -> None:
        chord = Chord(root=Note.new_c(), quality=Quality.Major)
        voicing = Voicing(chord=chord, inversion=Inversion.First, octave=4)
        pitches = voicing.to_pitches()
        assert pitches == [
            Pitch(note=Note.new_c(), octave=2),
            Pitch(note=Note.new_e(), octave=4),
            Pitch(note=Note.new_g(), octave=4),
            Pitch(note=Note.new_c(), octave=5),
        ]

    def test_get_pitches_third_inversion_major_chord_raises_value_error(self) -> None:
        chord = Chord(root=Note.new_c(), quality=Quality.Major)
        voicing = Voicing(chord=chord, inversion=Inversion.Third, octave=4)
        with pytest.raises(
            ValueError, match="The third inversion does not exist for a voicing with 3 right hand notes."
        ):
            voicing.to_pitches()

    def test_get_pitches_third_inversion(self) -> None:
        chord = Chord(root=Note.new_c(), quality=Quality.Major, extension=Extension.Seven)
        voicing = Voicing(chord=chord, inversion=Inversion.Second, octave=4)
        pitches = voicing.to_pitches()
        assert pitches == [
            Pitch(note=Note.new_c(), octave=2),
            Pitch(note=Note.new_g(), octave=4),
            Pitch(note=Note.new_a_sharp(), octave=4),
            Pitch(note=Note.new_c(), octave=5),
            Pitch(note=Note.new_e(), octave=5),
        ]

    @pytest.mark.skip(reason="Safe pitch transpose not yet implemented.")
    def test_get_pitches_flats(self) -> None:
        chord = Chord(root=Note.new_e_flat(), quality=Quality.Major)
        voicing = Voicing(chord=chord, inversion=Inversion.Root, octave=4)
        pitches = voicing.to_pitches()
        assert pitches == [
            Pitch(note=Note.new_e_flat(), octave=2),
            Pitch(note=Note.new_e_flat(), octave=4),
            Pitch(note=Note.new_g(), octave=4),
            Pitch(note=Note.new_b_flat(), octave=4),
        ]

    def test_get_pitches_sharps(self) -> None:
        chord = Chord(root=Note.new_g_sharp(), quality=Quality.Major)
        voicing = Voicing(chord=chord, inversion=Inversion.Root, octave=4)
        pitches = voicing.to_pitches()
        assert pitches == [
            Pitch(note=Note.new_g_sharp(), octave=2),
            Pitch(note=Note.new_g_sharp(), octave=4),
            Pitch(note=Note.new_c(), octave=5),
            Pitch(note=Note.new_d_sharp(), octave=5),
        ]
