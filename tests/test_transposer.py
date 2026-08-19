import logging

import pytest

from cadenza import Chord, Note, Pitch, Quality, Song, Transposer

logger = logging.getLogger(__name__)


class TestTransposer:
    def test_transpose_pitch_unsafe_basic(self) -> None:
        pitch_1 = Pitch(note=Note.new_c(), octave=4)
        pitch_2 = Transposer.transpose_pitch_unsafe(pitch_1, 1)
        assert pitch_2.note == Note.new_d_flat()
        assert pitch_2.octave == 4

    def test_transpose_pitch_unsafe_across_octaves(self) -> None:
        pitch_1 = Pitch(note=Note.new_g(), octave=3)
        pitch_2 = Transposer.transpose_pitch_unsafe(pitch_1, 6)
        assert pitch_2.note == Note.new_d_flat()
        assert pitch_2.octave == 4

    def test_transpose_pitch_unsafe_with_flat(self) -> None:
        pitch_1 = Pitch(note=Note.new_a_flat(), octave=4)
        pitch_2 = Transposer.transpose_pitch_unsafe(pitch_1, 7)
        assert pitch_2.note == Note.new_e_flat()
        assert pitch_2.octave == 5

    def test_transpose_power_chord_preserves_quality(self) -> None:
        chord = Chord.from_str("A5/E")
        transposed = Transposer.transpose_chord(chord, 3, tonic=Note.new_c())
        assert transposed.quality == Quality.Power
        assert transposed.root == Note.new_c()
        assert transposed.bass == Note.new_g()

    def test_transpose_chord_spells_bass_from_the_chord(self) -> None:
        # G# is the third of E7, so it stays G# even though that pitch class is the b6 of C
        chord = Chord.from_str("E7/G#")
        transposed = Transposer.transpose_chord(chord, 0, tonic=Note.new_c())
        assert transposed.to_str() == "E7/G♯"

    def test_transpose_chord_respells_a_bass_that_disagrees_with_its_chord(self) -> None:
        chord = Chord.from_str("E7/Ab")
        transposed = Transposer.transpose_chord(chord, 0, tonic=Note.new_c())
        assert transposed.to_str() == "E7/G♯"

    def test_transpose_chord_spells_a_non_chord_tone_bass_from_the_key(self) -> None:
        # F# is no part of a C major triad, so the key names it: the #4, not the b5
        chord = Chord.from_str("C/F#")
        transposed = Transposer.transpose_chord(chord, 0, tonic=Note.new_c())
        assert transposed.to_str() == "C/F♯"

    def test_transpose_chord_spells_root_from_the_key(self) -> None:
        chord = Chord.from_str("F#dim")
        transposed = Transposer.transpose_chord(chord, 0, tonic=Note.new_c())
        assert transposed.to_str() == "F♯°"

    def test_transpose_chord_unsafe_keeps_the_spelling_it_was_given(self) -> None:
        chord = Chord.from_str("E7/G#")
        assert Transposer.transpose_chord_unsafe(chord, 0).to_str() == "E7/G♯"
        assert Transposer.transpose_chord_unsafe(chord, 5).to_str() == "A7/C♯"

    def test_transpose_song_refuses_a_song_with_no_key(self) -> None:
        song = Song.model_validate({"id": "test", "title": "Keyless", "artist": "Test", "chords": "C F#dim G"})

        with pytest.raises(ValueError, match="no key"):
            Transposer.transpose_song(song, 2)

        transposed = Transposer.transpose_song_unsafe(song, 2)
        assert [chord.to_str() for chord in transposed.chords[0]] == ["D", "G♯°", "A"]

    @pytest.mark.parametrize(
        ("semitones", "tonic_str", "expected"),
        [
            (0, "C", "C G/B Am E7/G♯ C/E F F♯° C/G F/G C"),
            (2, "D", "D A/C♯ Bm F♯7/A♯ D/F♯ G G♯° D/A G/A D"),
            (5, "F", "F C/E Dm A7/C♯ F/A B♭ B° F/C B♭/C F"),
            (3, "Eb", "E♭ B♭/D Cm G7/B E♭/G A♭ A° E♭/B♭ A♭/B♭ E♭"),
        ],
    )
    def test_transpose_border_song(self, semitones: int, tonic_str: str, expected: str) -> None:
        # Border Song is in C major and leans on E7/G#, whose bass is the third of the chord
        chords = "C G/B Am E7/G# C/E F F#dim C/G F/G C"
        tonic = Note.from_str(tonic_str)
        transposed = [Transposer.transpose_chord(Chord.from_str(c), semitones, tonic=tonic) for c in chords.split()]
        assert " ".join(chord.to_str() for chord in transposed) == expected

    def test_transpose_cheap_date_keeps_a_chromatic_and_a_diatonic_diminished_apart(self) -> None:
        # Cheap Date is in D major and plays a G#dim and a Gdim two chords apart
        chords = "D/A Bm Em7 D/F# G G#dim A Gdim"
        transposed = [Transposer.transpose_chord(Chord.from_str(c), 0, tonic=Note.new_d()) for c in chords.split()]
        assert " ".join(chord.to_str() for chord in transposed) == "D/A Bm Em7 D/F♯ G G♯° A G°"

    def test_transpose_song_spells_the_destination_key(self) -> None:
        song = Song.model_validate(
            {
                "id": "test",
                "title": "Test",
                "artist": "Test",
                "chords": "C F#dim G",
                "key": {"root": "C", "mode": "major"},
            }
        )

        transposed = Transposer.transpose_song(song, 6)
        assert transposed.key is not None
        assert transposed.key.root == Note.new_g_flat()
        assert [chord.to_str() for chord in transposed.chords[0]] == ["G♭", "C°", "D♭"]

    def test_transpose_song_keeps_the_destination_key_readable(self) -> None:
        # A♭ up a semitone is A major, not the B♭♭ major the interval alone would name
        song = Song.model_validate(
            {
                "id": "test",
                "title": "Test",
                "artist": "Test",
                "chords": "Ab Db Eb",
                "key": {"root": "Ab", "mode": "major"},
            }
        )

        transposed = Transposer.transpose_song(song, 1)
        assert transposed.key is not None
        assert transposed.key.root == Note.new_a()
        assert [chord.to_str() for chord in transposed.chords[0]] == ["A", "D", "E"]

    @pytest.mark.parametrize(
        ("semitones", "tonic_str", "expected"),
        [
            (11, "B", "D♯7/F𝄪"),  # The third of D#7 is F double sharp, however it reads
            (6, "F#", "A♯7/C𝄪"),
        ],
    )
    def test_transpose_chord_into_a_double_accidental(self, semitones: int, tonic_str: str, expected: str) -> None:
        chord = Chord.from_str("E7/G#")
        transposed = Transposer.transpose_chord(chord, semitones, tonic=Note.from_str(tonic_str))
        assert transposed.to_str() == expected

        # Whatever we print has to parse back to the same chord
        assert Chord.from_str(transposed.to_str()) == transposed
        assert Chord.from_str(transposed.to_str(symbols=False)) == transposed

    def test_transpose_song_into_a_double_accidental_round_trips(self) -> None:
        song = Song.model_validate(
            {
                "id": "test",
                "title": "Test",
                "artist": "Test",
                "chords": "C E7/G# F#dim",
                "key": {"root": "C", "mode": "major"},
            }
        )

        transposed = Transposer.transpose_song(song, 11)
        printed = " ".join(chord.to_str() for chord in transposed.chords[0])
        assert printed == "B D♯7/F𝄪 E♯°"
        assert [Chord.from_str(token) for token in printed.split()] == transposed.chords[0]
