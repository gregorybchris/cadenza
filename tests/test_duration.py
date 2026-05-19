import pytest

from cadenza import Duration


class TestDuration:
    @pytest.mark.parametrize(
        ("duration", "expected"),
        [
            (Duration.Whole, 4.0),
            (Duration.Half, 2.0),
            (Duration.Quarter, 1.0),
            (Duration.Eighth, 0.5),
            (Duration.Sixteenth, 0.25),
            (Duration.ThirtySecond, 0.125),
        ],
    )
    def test_get_n_quarter_notes(self, duration: Duration, expected: float) -> None:
        assert duration.get_n_quarter_notes() == expected
