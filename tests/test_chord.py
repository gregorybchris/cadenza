from typing import Optional

import pytest

from cadenza import Alteration, Chord, Extension, Note, Quality
from cadenza.utils.symbol_utils import add_symbols, remove_symbols


class TestChord:
    @pytest.mark.parametrize(
        ("chord_str", "root", "quality", "extension", "alteration", "bass"),
        [
            ("Abm7", Note.A_FLAT, Quality.Minor, Extension.Seven, None, None),
            ("B7", Note.B, Quality.Major, Extension.Seven, None, None),
            ("Bbmaj7", Note.B_FLAT, Quality.Major, Extension.MajorSeven, None, None),
            ("C#dim", Note.C_SHARP, Quality.Diminished, None, None, None),
            ("Chalfdim", Note.C, Quality.HalfDiminished, None, None, None),
            ("D", Note.D, Quality.Major, None, None, None),
            ("D#aug", Note.D_SHARP, Quality.Augmented, None, None, None),
            ("Emaj7b5", Note.E, Quality.Major, Extension.MajorSeven, Alteration.FlatFive, None),
            ("Fsus2", Note.F, Quality.SusTwo, None, None, None),
            ("Gsus4", Note.G, Quality.SusFour, None, None, None),
            ("F/G", Note.F, Quality.Major, None, None, Note.G),
            ("Dm/F", Note.D, Quality.Minor, None, None, Note.F),
            ("E7b9/G#", Note.E, Quality.Major, Extension.Seven, Alteration.FlatNine, Note.G_SHARP),
            ("C9", Note.C, Quality.Major, Extension.Nine, None, None),
            ("C11", Note.C, Quality.Major, Extension.Eleven, None, None),
            ("C13", Note.C, Quality.Major, Extension.Thirteen, None, None),
            ("Aadd2", Note.A, Quality.Major, None, Alteration.AddTwo, None),
            ("Badd4", Note.B, Quality.Major, None, Alteration.AddFour, None),
            ("Cadd6", Note.C, Quality.Major, None, Alteration.AddSix, None),
            ("D2", Note.D, Quality.Major, None, Alteration.AddTwo, None),
            ("E4", Note.E, Quality.Major, None, Alteration.AddFour, None),
            ("F6", Note.F, Quality.Major, None, Alteration.AddSix, None),
            ("G7sus4", Note.G, Quality.SusFour, Extension.Seven, None, None),
            ("A7b5sus2/D#", Note.A, Quality.SusTwo, Extension.Seven, Alteration.FlatFive, Note.D_SHARP),
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
        ("chord", "expected_chord_str", "expected_chord_symbol_str"),
        [
            (
                Chord(
                    root=Note.D_SHARP,
                    quality=Quality.Augmented,
                    extension=None,
                    alteration=None,
                    bass=None,
                ),
                "D#aug",
                "D♯+",
            ),
            (
                Chord(
                    root=Note.E,
                    quality=Quality.Major,
                    extension=Extension.Seven,
                    alteration=Alteration.FlatNine,
                    bass=Note.G_SHARP,
                ),
                "E7b9/G#",
                "E7♭9/G♯",
            ),
            (
                Chord(
                    root=Note.A,
                    quality=Quality.SusTwo,
                    extension=Extension.Seven,
                    alteration=Alteration.FlatFive,
                    bass=Note.D_SHARP,
                ),
                "A7b5sus2/D#",
                "A7♭5sus2/D♯",
            ),
        ],
    )
    def test_to_str(self, chord: Chord, expected_chord_str: str, expected_chord_symbol_str: str) -> None:
        chord_str = str(chord)
        assert chord_str == expected_chord_str

        chord_symbol_str = chord.to_str(symbols=True)
        assert chord_symbol_str == expected_chord_symbol_str
