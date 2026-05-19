import pytest

from cadenza import NoteLetter


class TestNoteLetter:
    @pytest.mark.parametrize(
        ("note_letter", "expected"),
        [
            (NoteLetter.C, 0),
            (NoteLetter.D, 1),
            (NoteLetter.E, 2),
            (NoteLetter.F, 3),
            (NoteLetter.G, 4),
            (NoteLetter.A, 5),
            (NoteLetter.B, 6),
        ],
    )
    def test_to_index(self, note_letter: NoteLetter, expected: int) -> None:
        assert note_letter.to_index() == expected

    @pytest.mark.parametrize(
        ("index", "expected"),
        [
            (0, NoteLetter.C),
            (4, NoteLetter.G),
            (6, NoteLetter.B),
            (7, NoteLetter.C),
            (-1, NoteLetter.B),
        ],
    )
    def test_from_index(self, index: int, expected: NoteLetter) -> None:
        assert NoteLetter.from_index(index) == expected

    @pytest.mark.parametrize("note_letter", list(NoteLetter))
    def test_to_index_from_index_round_trip(self, note_letter: NoteLetter) -> None:
        assert NoteLetter.from_index(note_letter.to_index()) == note_letter

    @pytest.mark.parametrize(
        ("note_letter_str", "expected"),
        [
            ("A", NoteLetter.A),
            ("C", NoteLetter.C),
            ("G", NoteLetter.G),
        ],
    )
    def test_from_str(self, note_letter_str: str, expected: NoteLetter) -> None:
        assert NoteLetter.from_str(note_letter_str) == expected

    @pytest.mark.parametrize("note_letter", list(NoteLetter))
    def test_to_str(self, note_letter: NoteLetter) -> None:
        assert note_letter.to_str() == note_letter.value
