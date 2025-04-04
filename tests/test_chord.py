from typing import Optional

import pytest

from cadenza import Alteration, Chord, Extension, Note, Quality
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
            ("A7b5sus2/D#", Note.new_a(), Quality.SusTwo, Extension.Seven, Alteration.FlatFive, Note.new_d_sharp()),
            ("Eadd9", Note.new_e(), Quality.Major, None, Alteration.AddNine, None),
            ("Gbmaj9", Note.new_g_flat(), Quality.Major, Extension.MajorNine, None, None),
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
                "A7b5sus2/D#",
                "A7♭5sus2/D♯",
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
