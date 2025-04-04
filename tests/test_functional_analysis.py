import pytest

from cadenza import Chord, Note
from cadenza.functional_analysis import FunctionalAnalysis


class TestFunctionalAnalysis:
    @pytest.mark.parametrize(
        ("chord_str", "root", "expected"),
        [
            ("Abm7", Note.new_b_flat(), "vii7"),
            ("B7", Note.new_d(), "VI7"),
            ("Bbmaj7", Note.new_e_flat(), "Vmaj7"),
            ("C#dim", Note.new_g_sharp(), "iv°"),
            ("Chalfdim", Note.new_a(), "IIIø"),
            ("D", Note.new_e(), "VII"),
            ("D#aug", Note.new_d_flat(), "II+"),
            ("Emaj7b5", Note.new_f(), "VIImaj7"),
            ("Fsus2", Note.new_c_sharp(), "IIIsus2"),
            ("Gsus4", Note.new_f(), "IIsus4"),
            ("F/G", Note.new_a(), "VI/VII"),
            ("Dm/F", Note.new_a_flat(), "?"),
            ("E7b9/G#", Note.new_f(), "VII7/III"),
            ("C9", Note.new_d(), "VII9"),
            ("C11", Note.new_e(), "VI11"),
            ("C13", Note.new_a(), "III13"),
            ("Aadd2", Note.new_b(), "VII"),
            ("Badd4", Note.new_g(), "III"),
            ("Cadd6", Note.new_d(), "VII"),
            ("D2", Note.new_f(), "VI"),
            ("E4", Note.new_g(), "VI"),
            ("F6", Note.new_f_sharp(), "VII"),
            ("G7sus4", Note.new_a_sharp(), "VI7sus4"),
            ("A7b5sus2/D#", Note.new_a_flat(), "?"),
            ("Eadd9", Note.new_e(), "I"),
            ("Gbmaj9", Note.new_g(), "VIImaj9"),
            ("Cm9", Note.new_d(), "vii9"),
        ],
    )
    def test_get_chord_function_str(self, chord_str: str, root: Note, expected: str) -> None:
        chord = Chord.from_str(chord_str)
        function_str = FunctionalAnalysis.get_chord_function_str(chord, root)
        assert function_str == expected, (
            f"Expected '{expected}', but got '{function_str}' for chord '{chord_str}' and root '{root}'"
        )
