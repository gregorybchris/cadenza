import logging

import pytest

from cadenza import Note, Quality
from cadenza.core.speller import Speller

logger = logging.getLogger(__name__)


class TestSpeller:
    @pytest.mark.parametrize(
        ("pitch_class", "tonic_str", "expected_str"),
        [
            # The chromatic degrees of a major key take their usual spellings
            (1, "C", "Db"),
            (3, "C", "Eb"),
            (6, "C", "F#"),  # The leading tone into V, not a flattened fifth
            (8, "C", "Ab"),
            (10, "C", "Bb"),
            # Diatonic degrees always come back spelled as the key writes them
            (11, "C", "B"),
            (6, "G", "F#"),
            (10, "F", "Bb"),
            (11, "Gb", "Cb"),
            # A minor tonic uses the same letters as a major one
            (5, "A", "F"),
            (8, "A", "G#"),
        ],
    )
    def test_spell_from_tonic(self, pitch_class: int, tonic_str: str, expected_str: str) -> None:
        spelled = Speller.spell_from_tonic(pitch_class, Note.from_str(tonic_str))
        assert spelled == Note.from_str(expected_str)

    @pytest.mark.parametrize(
        ("pitch_class", "root_str", "expected_str"),
        [
            (8, "E", "G#"),  # The third of E7 is G#, whatever the key would call that pitch class
            (1, "A", "C#"),
            (10, "E", "Bb"),  # Measured from a root, a tritone is a flattened fifth
            (11, "Ab", "Cb"),
            (3, "Ab", "Eb"),
        ],
    )
    def test_spell_from_root(self, pitch_class: int, root_str: str, expected_str: str) -> None:
        spelled = Speller.spell_from_root(pitch_class, Note.from_str(root_str))
        assert spelled == Note.from_str(expected_str)

    @pytest.mark.parametrize(
        ("pitch_class", "tonic_str", "expected_str"),
        [
            (3, "G", "D#"),  # The leading tone chord into vi takes a raised fifth
            (6, "Bb", "F#"),
        ],
    )
    def test_spell_diminished_from_tonic(self, pitch_class: int, tonic_str: str, expected_str: str) -> None:
        spelled = Speller.spell_from_tonic(pitch_class, Note.from_str(tonic_str), Quality.Diminished)
        assert spelled == Note.from_str(expected_str)

    def test_spell_diminished_avoids_double_accidentals(self) -> None:
        # The raised fifth of F# major would be C##, so the flattened sixth reads better
        spelled = Speller.spell_from_tonic(2, Note.from_str("F#"), Quality.Diminished)
        assert spelled == Note.from_str("D")

    def test_spell_diminished_leaves_diatonic_degrees_alone(self) -> None:
        spelled = Speller.spell_from_tonic(11, Note.from_str("C"), Quality.Diminished)
        assert spelled == Note.new_b()
