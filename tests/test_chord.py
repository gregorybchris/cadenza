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
