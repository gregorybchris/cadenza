from cadenza.diatonic_mode import DiatonicMode
from cadenza.diatonic_scale import DiatonicScale
from cadenza.note import Note
from cadenza.note_letter import NoteLetter


class TestDiatonicScale:
    def test_get_notes_sharp(self) -> None:
        root = Note.new_e()
        mode = DiatonicMode.Aeolian
        scale = DiatonicScale(root=root, mode=mode)
        notes = scale.get_notes()
        assert notes == [
            Note.new_e(),
            Note.new_f_sharp(),
            Note.new_g(),
            Note.new_a(),
            Note.new_b(),
            Note.new_c(),
            Note.new_d(),
        ]

    def test_get_notes_flat(self) -> None:
        root = Note.new_f()
        mode = DiatonicMode.Ionian
        scale = DiatonicScale(root=root, mode=mode)
        notes = scale.get_notes()
        assert notes == [
            Note.new_f(),
            Note.new_g(),
            Note.new_a(),
            Note.new_b_flat(),
            Note.new_c(),
            Note.new_d(),
            Note.new_e(),
        ]

    def test_get_notes_double_flat(self) -> None:
        root = Note.new_e_flat()
        mode = DiatonicMode.Locrian
        scale = DiatonicScale(root=root, mode=mode)
        notes = scale.get_notes()
        assert notes == [
            Note(letter=NoteLetter.E, n_flats=1),
            Note(letter=NoteLetter.F, n_flats=1),
            Note(letter=NoteLetter.G, n_flats=1),
            Note(letter=NoteLetter.A, n_flats=1),
            Note(letter=NoteLetter.B, n_flats=2),
            Note(letter=NoteLetter.C, n_flats=1),
            Note(letter=NoteLetter.D, n_flats=1),
        ]
