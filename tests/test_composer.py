import logging
import math

import pytest

from cadenza import Alteration, Chord, Composer, Extension, Inversion, Note, Pitch, Quality, Voicing
from cadenza.note_letter import NoteLetter

logger = logging.getLogger(__name__)


class TestComposer:
    def test_pitch_to_frequency(self) -> None:
        concert_a_pitch = Pitch(note=Note.new_a(), octave=4)
        concert_a_frequency = Composer.pitch_to_frequency(concert_a_pitch)
        assert math.isclose(concert_a_frequency, 440.0, rel_tol=1e-3)

    def test_frequency_to_pitch(self) -> None:
        concert_a_frequency = 440.0
        concert_a_pitch = Composer.frequency_to_pitch(concert_a_frequency)
        assert concert_a_pitch.note == Note.new_a()
        assert concert_a_pitch.octave == 4

    def test_frequency_to_pitch_low_c(self) -> None:
        low_c_frequency = 32.7
        low_c_pitch = Composer.frequency_to_pitch(low_c_frequency)
        assert low_c_pitch.note == Note.new_c()
        assert low_c_pitch.octave == 1

    def test_voicing_to_pitches_root(self) -> None:
        chord = Chord(root=Note.new_c(), quality=Quality.Major)
        voicing = Voicing(chord=chord, inversion=Inversion.Root, octave=4)
        pitches = Composer.voicing_to_pitches(voicing)
        assert pitches == [
            Pitch(note=Note.new_c(), octave=2),
            Pitch(note=Note.new_c(), octave=4),
            Pitch(note=Note.new_e(), octave=4),
            Pitch(note=Note.new_g(), octave=4),
        ]

    def test_voicing_to_pitches_first_inversion(self) -> None:
        chord = Chord(root=Note.new_c(), quality=Quality.Major)
        voicing = Voicing(chord=chord, inversion=Inversion.First, octave=4)
        pitches = Composer.voicing_to_pitches(voicing)
        assert pitches == [
            Pitch(note=Note.new_c(), octave=2),
            Pitch(note=Note.new_e(), octave=4),
            Pitch(note=Note.new_g(), octave=4),
            Pitch(note=Note.new_c(), octave=5),
        ]

    def test_voicing_to_pitches_third_inversion_major_chord_raises_value_error(self) -> None:
        chord = Chord(root=Note.new_c(), quality=Quality.Major)
        voicing = Voicing(chord=chord, inversion=Inversion.Third, octave=4)
        with pytest.raises(
            ValueError, match="The third inversion does not exist for a voicing with 3 right hand notes."
        ):
            Composer.voicing_to_pitches(voicing)

    def test_voicing_to_pitches_third_inversion(self) -> None:
        chord = Chord(root=Note.new_c(), quality=Quality.Major, extension=Extension.Seven)
        voicing = Voicing(chord=chord, inversion=Inversion.Second, octave=4)
        pitches = Composer.voicing_to_pitches(voicing)
        assert pitches == [
            Pitch(note=Note.new_c(), octave=2),
            Pitch(note=Note.new_g(), octave=4),
            Pitch(note=Note.new_b_flat(), octave=4),
            Pitch(note=Note.new_c(), octave=5),
            Pitch(note=Note.new_e(), octave=5),
        ]

    def test_voicing_to_pitches_flats(self) -> None:
        chord = Chord(root=Note.new_e_flat(), quality=Quality.Major)
        voicing = Voicing(chord=chord, inversion=Inversion.Root, octave=4)
        pitches = Composer.voicing_to_pitches(voicing)
        assert pitches == [
            Pitch(note=Note.new_e_flat(), octave=2),
            Pitch(note=Note.new_e_flat(), octave=4),
            Pitch(note=Note.new_g(), octave=4),
            Pitch(note=Note.new_b_flat(), octave=4),
        ]

    def test_voicing_to_pitches_sharps(self) -> None:
        chord = Chord(root=Note.new_g_sharp(), quality=Quality.Major)
        voicing = Voicing(chord=chord, inversion=Inversion.Root, octave=4)
        pitches = Composer.voicing_to_pitches(voicing)
        assert pitches == [
            Pitch(note=Note(letter=NoteLetter.G, n_sharps=1), octave=2),
            Pitch(note=Note(letter=NoteLetter.G, n_sharps=1), octave=4),
            Pitch(note=Note(letter=NoteLetter.B, n_sharps=1), octave=5),
            Pitch(note=Note(letter=NoteLetter.D, n_sharps=1), octave=5),
        ]

    def test_voicing_to_pitches_flat_five(self) -> None:
        chord = Chord(root=Note.new_c(), quality=Quality.Major, alteration=Alteration.FlatFive)
        voicing = Voicing(chord=chord, inversion=Inversion.Root, octave=4)
        pitches = Composer.voicing_to_pitches(voicing)
        assert pitches == [
            Pitch(note=Note.new_c(), octave=2),
            Pitch(note=Note.new_c(), octave=4),
            Pitch(note=Note.new_e(), octave=4),
            Pitch(note=Note.new_g_flat(), octave=4),
        ]
