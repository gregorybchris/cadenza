from typing import Optional

import pytest

from cadenza import Alteration, Chord, Extension, Note, NoteLetter, Quality
from cadenza.utils.symbol_utils import add_symbols, remove_symbols


class TestChord:
    @pytest.mark.parametrize(
        ("chord_str", "root", "quality", "extension", "alteration", "bass"),
        [
            ("Abm7", Note.new_a_flat(), Quality.Minor, Extension.Seven, None, None),
            ("B7", Note.new_b(), Quality.Major, Extension.Seven, None, None),
            ("Bbmaj7", Note.new_b_flat(), Quality.Major, Extension.MajorSeven, None, None),
            ("C#dim", Note.new_c_sharp(), Quality.Diminished, None, None, None),
            ("Chalfdim", Note.new_c(), Quality.HalfDiminished, None, None, None),
            ("D", Note.new_d(), Quality.Major, None, None, None),
            ("D#aug", Note.new_d_sharp(), Quality.Augmented, None, None, None),
            ("Emaj7b5", Note.new_e(), Quality.Major, Extension.MajorSeven, Alteration.FlatFive, None),
            ("Fsus2", Note.new_f(), Quality.SusTwo, None, None, None),
            ("Gsus4", Note.new_g(), Quality.SusFour, None, None, None),
            ("F/G", Note.new_f(), Quality.Major, None, None, Note.new_g()),
            ("Dm/F", Note.new_d(), Quality.Minor, None, None, Note.new_f()),
            ("E7b9/G#", Note.new_e(), Quality.Major, Extension.Seven, Alteration.FlatNine, Note.new_g_sharp()),
            ("C9", Note.new_c(), Quality.Major, Extension.Nine, None, None),
            ("C11", Note.new_c(), Quality.Major, Extension.Eleven, None, None),
            ("C13", Note.new_c(), Quality.Major, Extension.Thirteen, None, None),
            ("Aadd2", Note.new_a(), Quality.Major, None, Alteration.AddTwo, None),
            ("Badd4", Note.new_b(), Quality.Major, None, Alteration.AddFour, None),
            ("Cadd6", Note.new_c(), Quality.Major, None, Alteration.AddSix, None),
            ("D2", Note.new_d(), Quality.Major, None, Alteration.AddTwo, None),
            ("E4", Note.new_e(), Quality.Major, None, Alteration.AddFour, None),
            ("F6", Note.new_f(), Quality.Major, None, Alteration.AddSix, None),
            ("G7sus4", Note.new_g(), Quality.SusFour, Extension.Seven, None, None),
            ("A7sus2b5/D#", Note.new_a(), Quality.SusTwo, Extension.Seven, Alteration.FlatFive, Note.new_d_sharp()),
            ("G7sus4b9", Note.new_g(), Quality.SusFour, Extension.Seven, Alteration.FlatNine, None),
            ("Eadd9", Note.new_e(), Quality.Major, None, Alteration.AddNine, None),
            ("Gbmaj9", Note.new_g_flat(), Quality.Major, Extension.MajorNine, None, None),
            ("A5", Note.new_a(), Quality.Power, None, None, None),
            ("C#5", Note.new_c_sharp(), Quality.Power, None, None, None),
            ("Bb5", Note.new_b_flat(), Quality.Power, None, None, None),
            ("E5/B", Note.new_e(), Quality.Power, None, None, Note.new_b()),
            ("C57", Note.new_c(), Quality.Power, Extension.Seven, None, None),
            ("D5add9", Note.new_d(), Quality.Power, None, Alteration.AddNine, None),
            ("F57b5/A", Note.new_f(), Quality.Power, Extension.Seven, Alteration.FlatFive, Note.new_a()),
        ],
    )
    def test_from_str(  # noqa: PLR0913
        self,
        chord_str: str,
        root: Note,
        quality: Quality,
        extension: Optional[Extension],
        alteration: Optional[Alteration],
        bass: Optional[Note],
    ) -> None:
        chord_a = Chord.from_str(chord_str)
        assert chord_a.root == root
        assert chord_a.quality == quality
        assert chord_a.extension == extension
        assert chord_a.alteration == alteration
        assert chord_a.bass == bass

        chord_b = Chord.from_str(add_symbols(chord_str))
        assert chord_b == chord_a

        chord_c = Chord.from_str(remove_symbols(chord_str))
        assert chord_c == chord_a

    @pytest.mark.parametrize(
        ("chord", "expected_chord_str_no_symbols", "expected_chord_str_with_symbols"),
        [
            (Chord(root=Note.new_d_sharp(), quality=Quality.Augmented), "D#aug", "D♯+"),
            (Chord(root=Note.new_f(), quality=Quality.Diminished), "Fdim", "F°"),
            (Chord(root=Note.new_a(), quality=Quality.Minor), "Am", "Am"),
            (
                Chord(
                    root=Note.new_e(),
                    quality=Quality.Major,
                    extension=Extension.Seven,
                    alteration=Alteration.FlatNine,
                    bass=Note.new_g_sharp(),
                ),
                "E7b9/G#",
                "E7♭9/G♯",
            ),
            (
                Chord(
                    root=Note.new_a(),
                    quality=Quality.SusTwo,
                    extension=Extension.Seven,
                    alteration=Alteration.FlatFive,
                    bass=Note.new_d_sharp(),
                ),
                "A7sus2b5/D#",
                "A7sus2♭5/D♯",
            ),
            (Chord(root=Note.new_a(), quality=Quality.Power), "A5", "A5"),
            (
                Chord(root=Note.new_d(), quality=Quality.Major, alteration=Alteration.AddFour),
                "Dadd4",
                "Dadd4",
            ),
            (
                Chord(root=Note.new_c(), quality=Quality.Major, alteration=Alteration.AddTwo),
                "Cadd2",
                "Cadd2",
            ),
            (
                Chord(root=Note.new_g_sharp(), quality=Quality.Power, bass=Note.new_d_sharp()),
                "G#5/D#",
                "G♯5/D♯",
            ),
            (
                Chord(
                    root=Note.new_c(),
                    quality=Quality.Power,
                    extension=Extension.Seven,
                    alteration=Alteration.AddNine,
                ),
                "C57add9",
                "C57add9",
            ),
        ],
    )
    def test_to_str(
        self,
        chord: Chord,
        expected_chord_str_no_symbols: str,
        expected_chord_str_with_symbols: str,
    ) -> None:
        chord_str = str(chord)
        assert chord_str == expected_chord_str_with_symbols

        chord_symbol_str = chord.to_str(symbols=False)
        assert chord_symbol_str == expected_chord_str_no_symbols

    @pytest.mark.parametrize(
        ("chord_str", "expected"),
        [
            # The three ways a double accidental can be written all parse the same
            ("F##", "F𝄪"),
            ("F♯♯", "F𝄪"),
            ("F𝄪", "F𝄪"),
            ("Bbb", "B𝄫"),
            ("B♭♭", "B𝄫"),
            ("B𝄫", "B𝄫"),
            # Doubled accidentals on a bass note, which is where transposition produces them
            ("D#7/F##", "D♯7/F𝄪"),
            ("D♯7/F𝄪", "D♯7/F𝄪"),
            ("A♯7/C𝄪", "A♯7/C𝄪"),
            # Alongside every other part of a chord
            ("F##m7/A#", "F𝄪m7/A♯"),
            ("C𝄫maj7", "C𝄫maj7"),
            ("G𝄪sus4/B𝄪", "G𝄪sus4/B𝄪"),
        ],
    )
    def test_from_str_with_double_accidentals(self, chord_str: str, expected: str) -> None:
        assert Chord.from_str(chord_str).to_str() == expected

    @pytest.mark.parametrize(
        ("chord_str", "n_sharps", "n_flats"),
        [("F##", 2, 0), ("Bbb", 0, 2), ("C𝄪", 2, 0), ("C𝄫", 0, 2)],
    )
    def test_double_accidentals_reach_the_root(self, chord_str: str, n_sharps: int, n_flats: int) -> None:
        root = Chord.from_str(chord_str).root
        assert root.n_sharps == n_sharps
        assert root.n_flats == n_flats

    @pytest.mark.parametrize(
        ("chord_str", "expected_root", "expected_alteration"),
        [
            # A written-out double accidental followed by a digit is an alteration, not a double
            ("Ebb9", Note.new_e_flat(), Alteration.FlatNine),
            ("Ebb5", Note.new_e_flat(), Alteration.FlatFive),
            ("Abb9", Note.new_a_flat(), Alteration.FlatNine),
        ],
    )
    def test_written_out_accidentals_do_not_swallow_an_alteration(
        self, chord_str: str, expected_root: Note, expected_alteration: Alteration
    ) -> None:
        chord = Chord.from_str(chord_str)
        assert chord.root == expected_root
        assert chord.alteration == expected_alteration

    @pytest.mark.parametrize(
        ("chord_str", "expected_root", "expected_extension", "expected_alteration"),
        [
            # b5 and b9 are the only flattened alterations, so nothing else can be confused for one
            ("Bbb6", Note(letter=NoteLetter.B, n_flats=2), None, Alteration.AddSix),
            ("Ebb2", Note(letter=NoteLetter.E, n_flats=2), None, Alteration.AddTwo),
            ("Bbb7", Note(letter=NoteLetter.B, n_flats=2), Extension.Seven, None),
            ("Bbb11", Note(letter=NoteLetter.B, n_flats=2), Extension.Eleven, None),
            # No alteration may follow a sharp at all, so a doubled sharp never needs disambiguating
            ("C##9", Note(letter=NoteLetter.C, n_sharps=2), Extension.Nine, None),
        ],
    )
    def test_written_out_accidentals_only_yield_where_an_alteration_could_follow(
        self,
        chord_str: str,
        expected_root: Note,
        expected_extension: Optional[Extension],
        expected_alteration: Optional[Alteration],
    ) -> None:
        chord = Chord.from_str(chord_str)
        assert chord.root == expected_root
        assert chord.extension == expected_extension
        assert chord.alteration == expected_alteration

    @pytest.mark.parametrize(("chord_str", "expected_extension"), [("E𝄫9", Extension.Nine), ("E𝄫5", None)])
    def test_single_glyph_accidental_is_read_before_an_alteration(
        self, chord_str: str, expected_extension: Optional[Extension]
    ) -> None:
        # Nothing else 𝄫 could mean, so it wins even with a digit behind it
        chord = Chord.from_str(chord_str)
        assert chord.root == Note(letter=NoteLetter.E, n_flats=2)
        assert chord.extension == expected_extension
        assert chord.alteration is None

    @pytest.mark.parametrize(
        "chord_str",
        ["F##", "Bbb", "D#7/F##", "F##m7/A#", "C𝄫maj7", "G𝄪sus4/B𝄪", "A♯7/C𝄪"],
    )
    def test_double_accidental_round_trip(self, chord_str: str) -> None:
        chord = Chord.from_str(chord_str)
        assert Chord.from_str(chord.to_str()) == chord
        assert Chord.from_str(chord.to_str(symbols=False)) == chord

    @pytest.mark.parametrize("n_accidentals", [0, 1, 2])
    @pytest.mark.parametrize("suffix", ["", "m", "dim", "aug", "sus4", "7", "maj7", "9", "6", "m7/A#"])
    def test_every_accidental_round_trips_through_the_symbol_rendering(self, n_accidentals: int, suffix: str) -> None:
        for letter in NoteLetter:
            for n_sharps, n_flats in [(n_accidentals, 0), (0, n_accidentals)]:
                root = Note(letter=letter, n_sharps=n_sharps, n_flats=n_flats)
                chord = Chord.from_str(f"{root.to_str()}{suffix}")
                assert chord.root == root
                assert Chord.from_str(chord.to_str()) == chord

    @pytest.mark.parametrize("n_accidentals", [0, 1, 2])
    @pytest.mark.parametrize("suffix", ["", "m", "dim", "aug", "sus4", "7", "maj7", "6", "m7/A#"])
    def test_every_accidental_round_trips_written_out_too(self, n_accidentals: int, suffix: str) -> None:
        # NOTE: The 9 and 5 suffixes are left out, being the one case a written-out double flat
        # cannot survive. See test_a_written_out_double_flat_cannot_be_told_from_a_flattened_ninth.
        for letter in NoteLetter:
            for n_sharps, n_flats in [(n_accidentals, 0), (0, n_accidentals)]:
                root = Note(letter=letter, n_sharps=n_sharps, n_flats=n_flats)
                chord = Chord.from_str(f"{root.to_str()}{suffix}")
                assert Chord.from_str(chord.to_str(symbols=False)) == chord

    def test_a_written_out_double_flat_cannot_be_told_from_a_flattened_ninth(self) -> None:
        # Abb9 is equally an A𝄫 ninth and an A♭ with a flattened ninth. The latter is what anyone
        # writing it by hand means, so it wins, and the symbol is the only lossless way to write
        # the former. Double sharps have no such problem, no alteration being able to follow one.
        double_flat_ninth = Chord.from_str("A𝄫9")
        assert double_flat_ninth.root == Note(letter=NoteLetter.A, n_flats=2)
        assert double_flat_ninth.extension == Extension.Nine

        assert Chord.from_str(double_flat_ninth.to_str()) == double_flat_ninth
        assert double_flat_ninth.to_str(symbols=False) == "Abb9"

        written_out = Chord.from_str("Abb9")
        assert written_out.root == Note.new_a_flat()
        assert written_out.extension is None
        assert written_out.alteration == Alteration.FlatNine

        assert Chord.from_str("C𝄪9") == Chord.from_str("C##9")
