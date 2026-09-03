import pytest

from cadenza import Chord, FunctionalAnalysis, Note


class TestFunctionalAnalysis:
    @pytest.mark.parametrize(
        ("chord_str", "root", "expected"),
        [
            ("Abm7", Note.new_b_flat(), "vii7"),
            ("B7", Note.new_d(), "VI7"),
            ("Bbmaj7", Note.new_e_flat(), "Vmaj7"),
            ("C#dim", Note.new_g_sharp(), "iv°"),
            ("Chalfdim", Note.new_a(), "iiiø"),
            ("D", Note.new_e(), "VII"),
            ("D#aug", Note.new_d_flat(), "II+"),
            ("Emaj7b5", Note.new_f(), "VIImaj7♭5"),
            ("Fsus2", Note.new_c_sharp(), "IIIsus2"),
            ("Gsus4", Note.new_f(), "IIsus4"),
            ("F/G", Note.new_a(), "VI/VII"),
            ("Dm/F", Note.new_a_flat(), "?"),
            ("E7b9/G#", Note.new_f(), "VII7♭9/III"),
            ("C9", Note.new_d(), "VII9"),
            ("C11", Note.new_e(), "VI11"),
            ("C13", Note.new_a(), "III13"),
            ("Aadd2", Note.new_b(), "VIIadd2"),
            ("Badd4", Note.new_g(), "IIIadd4"),
            ("Cadd6", Note.new_d(), "VII6"),
            ("D2", Note.new_f(), "VIadd2"),
            ("E4", Note.new_g(), "VIadd4"),
            ("F6", Note.new_f_sharp(), "VII6"),
            ("G7sus4", Note.new_a_sharp(), "VI7sus4"),
            ("A7sus2b5/D#", Note.new_a_flat(), "?"),
            ("G7sus4b9", Note.new_c(), "V7sus4♭9"),
            ("Eadd9", Note.new_e(), "Iadd9"),
            ("Gbmaj9", Note.new_g(), "VIImaj9"),
            ("Cm9", Note.new_d(), "vii9"),
            ("C5", Note.new_c(), "I5"),
            ("A5", Note.new_d(), "V5"),
            ("G5/D", Note.new_c(), "V5/II"),
        ],
    )
    def test_get_chord_function_str(self, chord_str: str, root: Note, expected: str) -> None:
        chord = Chord.from_str(chord_str)
        function_str = FunctionalAnalysis.get_chord_function_str(chord, root)
        assert function_str == expected, (
            f"Expected '{expected}', but got '{function_str}' for chord '{chord_str}' and root '{root}'"
        )
