import pytest

from cadenza import Note, NoteLetter


class TestNote:
    @pytest.mark.parametrize(
        ("note_str", "expected"),
        [
            ("C", Note.new_c()),
            ("C#", Note.new_c_sharp()),
            ("Db", Note.new_d_flat()),
            ("F#", Note.new_f_sharp()),
            ("Bb", Note.new_b_flat()),
            ("C♯", Note.new_c_sharp()),
            ("D♭", Note.new_d_flat()),
            ("Bbb", Note(letter=NoteLetter.B, n_flats=2)),
            ("F##", Note(letter=NoteLetter.F, n_sharps=2)),
            ("B♭♭", Note(letter=NoteLetter.B, n_flats=2)),
            ("F♯♯", Note(letter=NoteLetter.F, n_sharps=2)),
            ("B𝄫", Note(letter=NoteLetter.B, n_flats=2)),
            ("F𝄪", Note(letter=NoteLetter.F, n_sharps=2)),
        ],
    )
    def test_from_str(self, note_str: str, expected: Note) -> None:
        assert Note.from_str(note_str) == expected

    @pytest.mark.parametrize(
        ("note", "expected_no_symbols", "expected_with_symbols"),
        [
            (Note.new_c(), "C", "C"),
            (Note.new_c_sharp(), "C#", "C♯"),
            (Note.new_d_flat(), "Db", "D♭"),
            (Note(letter=NoteLetter.B, n_flats=2), "Bbb", "B𝄫"),
            (Note(letter=NoteLetter.F, n_sharps=2), "F##", "F𝄪"),
        ],
    )
    def test_to_str(self, note: Note, expected_no_symbols: str, expected_with_symbols: str) -> None:
        assert str(note) == expected_with_symbols
        assert note.to_str(symbols=False) == expected_no_symbols

    @pytest.mark.parametrize(
        ("note", "expected"),
        [
            (Note.new_c(), 0),
            (Note.new_c_sharp(), 1),
            (Note.new_d_flat(), 1),
            (Note.new_e(), 4),
            (Note.new_g(), 7),
            (Note.new_b(), 11),
            (Note.new_b_sharp(), 0),
            (Note.new_c_flat(), 11),
        ],
    )
    def test_to_integer(self, note: Note, expected: int) -> None:
        assert note.to_integer() == expected

    @pytest.mark.parametrize(
        ("index", "expected"),
        [
            (0, Note.new_c()),
            (1, Note.new_d_flat()),
            (6, Note.new_g_flat()),
            (11, Note.new_b()),
            (12, Note.new_c()),
            (-1, Note.new_b()),
        ],
    )
    def test_from_integer_unsafe(self, index: int, expected: Note) -> None:
        assert Note.from_integer_unsafe(index) == expected

    @pytest.mark.parametrize(
        ("note", "other", "expected"),
        [
            (Note.new_c_sharp(), Note.new_d_flat(), True),
            (Note.new_b_sharp(), Note.new_c(), True),
            (Note.new_c(), Note.new_c(), True),
            (Note.new_c(), Note.new_d(), False),
        ],
    )
    def test_is_enharmonic(self, note: Note, other: Note, expected: bool) -> None:
        assert note.is_enharmonic(other) == expected

    @pytest.mark.parametrize(
        ("note_str", "expected"),
        [
            ("C𝄪", 2),
            ("C𝄫", 10),
            ("F𝄪", 7),
            ("B𝄪", 1),
            ("C♭", 11),
            ("B♯", 0),
        ],
    )
    def test_to_integer_with_double_accidentals(self, note_str: str, expected: int) -> None:
        assert Note.from_str(note_str).to_integer() == expected

    @pytest.mark.parametrize("n_sharps", [0, 1, 2])
    @pytest.mark.parametrize("n_flats", [0, 1, 2])
    def test_double_accidental_round_trip(self, n_sharps: int, n_flats: int) -> None:
        if n_sharps and n_flats:
            # A note is spelled with sharps or with flats, never both
            return
        note = Note(letter=NoteLetter.G, n_sharps=n_sharps, n_flats=n_flats)
        assert Note.from_str(note.to_str()) == note
        assert Note.from_str(note.to_str(symbols=False)) == note
