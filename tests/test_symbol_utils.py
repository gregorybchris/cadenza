import pytest

from cadenza.utils.symbol_utils import add_symbols, remove_symbols


class TestSymbolUtils:
    @pytest.mark.parametrize(
        ("plain", "with_symbols"),
        [
            ("C#", "C♯"),
            ("Bb", "B♭"),
            ("C#dim", "C♯°"),
            ("Chalfdim", "Cø"),
            ("D#aug", "D♯+"),
            ("Am", "Am"),
            ("E7b9/G#", "E7♭9/G♯"),
            ("D", "D"),
            ("F##", "F𝄪"),
            ("Bbb", "B𝄫"),
            ("D#7/F##", "D♯7/F𝄪"),
            ("Fbb", "F𝄫"),
        ],
    )
    def test_add_symbols(self, plain: str, with_symbols: str) -> None:
        assert add_symbols(plain) == with_symbols

    @pytest.mark.parametrize(
        ("plain", "with_symbols"),
        [
            ("C#", "C♯"),
            ("Bb", "B♭"),
            ("C#dim", "C♯°"),
            ("Chalfdim", "Cø"),
            ("D#aug", "D♯+"),
            ("Am", "Am"),
            ("E7b9/G#", "E7♭9/G♯"),
            ("D", "D"),
            ("F##", "F𝄪"),
            ("Bbb", "B𝄫"),
            ("D#7/F##", "D♯7/F𝄪"),
            ("Fbb", "F𝄫"),
        ],
    )
    def test_remove_symbols(self, plain: str, with_symbols: str) -> None:
        assert remove_symbols(with_symbols) == plain

    @pytest.mark.parametrize(
        "plain",
        ["C#", "Bb", "C#dim", "Chalfdim", "D#aug", "Am", "E7b9/G#", "D", "F##", "Bbb", "D#7/F##", "Fbb"],
    )
    def test_add_then_remove_round_trip(self, plain: str) -> None:
        assert remove_symbols(add_symbols(plain)) == plain

    @pytest.mark.parametrize(
        ("written_out", "single_glyph"),
        [("F♯♯", "F𝄪"), ("B♭♭", "B𝄫")],
    )
    def test_remove_symbols_accepts_a_doubled_single_accidental(self, written_out: str, single_glyph: str) -> None:
        assert remove_symbols(written_out) == remove_symbols(single_glyph)
