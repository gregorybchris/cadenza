from cadenza.diatonic_mode import DiatonicMode
from cadenza.diatonic_scale import DiatonicScale
from cadenza.note import Note


class TestDiatonicScale:
    def test_get_notes_sharp(self) -> None:
        root = Note.E
        mode = DiatonicMode.Aeolian
        scale = DiatonicScale(root=root, mode=mode)
        notes = scale.get_notes()
        assert notes == [
            Note.E,
            Note.FSharp,
            Note.G,
            Note.A,
            Note.B,
            Note.C,
            Note.D,
            Note.E,
        ]

    def test_get_notes_flat(self) -> None:
        root = Note.F
        mode = DiatonicMode.Ionian
        scale = DiatonicScale(root=root, mode=mode)
        notes = scale.get_notes()
        assert notes == [
            Note.F,
            Note.G,
            Note.A,
            # TODO: Fix this test to use BFlat instead of ASharp
            Note.ASharp,
            Note.C,
            Note.D,
            Note.E,
            Note.F,
        ]
