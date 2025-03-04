import pytest

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

    def test_get_key_signature_flats_major(self) -> None:
        root = Note.new_e_flat()
        mode = DiatonicMode.Ionian
        scale = DiatonicScale(root=root, mode=mode)
        key_signature = scale.get_key_signature()
        assert key_signature == [
            Note.new_b_flat(),
            Note.new_e_flat(),
            Note.new_a_flat(),
        ]

    def test_get_key_signature_sharps_major(self) -> None:
        root = Note.new_e()
        mode = DiatonicMode.Ionian
        scale = DiatonicScale(root=root, mode=mode)
        key_signature = scale.get_key_signature()
        assert key_signature == [
            Note.new_f_sharp(),
            Note.new_c_sharp(),
            Note.new_g_sharp(),
            Note.new_d_sharp(),
        ]

    def test_get_key_signature_flats_minor(self) -> None:
        root = Note.new_d()
        mode = DiatonicMode.Aeolian
        scale = DiatonicScale(root=root, mode=mode)
        key_signature = scale.get_key_signature()
        assert key_signature == [
            Note.new_b_flat(),
        ]

    def test_get_key_signature_sharps_minor(self) -> None:
        root = Note.new_g_sharp()
        mode = DiatonicMode.Aeolian
        scale = DiatonicScale(root=root, mode=mode)
        key_signature = scale.get_key_signature()
        assert key_signature == [
            Note.new_f_sharp(),
            Note.new_c_sharp(),
            Note.new_g_sharp(),
            Note.new_d_sharp(),
            Note.new_a_sharp(),
        ]

    def test_get_invalid_key_signature(self) -> None:
        root = Note.new_e_flat()
        mode = DiatonicMode.Locrian
        scale = DiatonicScale(root=root, mode=mode)
        msg = "The diatonic scale E♭ locrian has a double flat and does not have a standard key signature."
        with pytest.raises(ValueError, match=msg):
            scale.get_key_signature()
