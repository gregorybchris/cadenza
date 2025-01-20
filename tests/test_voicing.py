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
        chord = Chord(root=Note.C, quality=Quality.Major)
        voicing = Voicing(chord=chord, inversion=Inversion.Root, octave=4)
        pitches = voicing.get_pitches()
        assert pitches == [
            Pitch(note=Note.C, octave=2),
            Pitch(note=Note.C, octave=4),
            Pitch(note=Note.E, octave=4),
            Pitch(note=Note.G, octave=4),
        ]

    def test_get_pitches_first_inversion(self) -> None:
        chord = Chord(root=Note.C, quality=Quality.Major)
        voicing = Voicing(chord=chord, inversion=Inversion.First, octave=4)
        pitches = voicing.get_pitches()
        assert pitches == [
            Pitch(note=Note.C, octave=2),
            Pitch(note=Note.E, octave=4),
            Pitch(note=Note.G, octave=4),
            Pitch(note=Note.C, octave=5),
        ]

    def test_get_pitches_third_inversion_major_chord_raises_value_error(self) -> None:
        chord = Chord(root=Note.C, quality=Quality.Major)
        voicing = Voicing(chord=chord, inversion=Inversion.Third, octave=4)
        with pytest.raises(
            ValueError, match="The third inversion does not exist for a voicing with 3 right hand notes."
        ):
            voicing.get_pitches()

    def test_get_pitches_third_inversion(self) -> None:
        chord = Chord(root=Note.C, quality=Quality.Major, extension=Extension.Seven)
        voicing = Voicing(chord=chord, inversion=Inversion.Second, octave=4)
        pitches = voicing.get_pitches()
        assert pitches == [
            Pitch(note=Note.C, octave=2),
            Pitch(note=Note.G, octave=4),
            Pitch(note=Note.A_SHARP, octave=4),
            Pitch(note=Note.C, octave=5),
            Pitch(note=Note.E, octave=5),
        ]

    def test_get_pitches_flats(self) -> None:
        chord = Chord(root=Note.E_FLAT, quality=Quality.Major)
        voicing = Voicing(chord=chord, inversion=Inversion.Root, octave=4)
        pitches = voicing.get_pitches()
        assert pitches == [
            Pitch(note=Note.E_FLAT, octave=2),
            Pitch(note=Note.E_FLAT, octave=4),
            Pitch(note=Note.G, octave=4),
            Pitch(note=Note.B_FLAT, octave=4),
        ]

    def test_get_pitches_sharps(self) -> None:
        chord = Chord(root=Note.G_SHARP, quality=Quality.Major)
        voicing = Voicing(chord=chord, inversion=Inversion.Root, octave=4)
        pitches = voicing.get_pitches()
        assert pitches == [
            Pitch(note=Note.G_SHARP, octave=2),
            Pitch(note=Note.G_SHARP, octave=4),
            Pitch(note=Note.C, octave=4),
            Pitch(note=Note.D_SHARP, octave=4),
        ]
