import pytest

from cadenza import Interval, ParseError


class TestInterval:
    @pytest.mark.parametrize(
        ("interval", "expected"),
        [
            (Interval.Unison, "unison"),
            (Interval.MinorThird, "minor third"),
            (Interval.PerfectFifth, "perfect fifth"),
            (Interval.Tritone, "tritone"),
            (Interval.Octave, "octave"),
            (Interval.AugmentedEleventh, "augmented eleventh"),
            (Interval.MajorThirteenth, "major thirteenth"),
        ],
    )
    def test_to_written(self, interval: Interval, expected: str) -> None:
        assert interval.to_written() == expected

    @pytest.mark.parametrize(
        ("interval_str", "expected"),
        [
            ("P1", Interval.Unison),
            ("m3", Interval.MinorThird),
            ("TT", Interval.Tritone),
            ("P8", Interval.Octave),
            ("M13", Interval.MajorThirteenth),
        ],
    )
    def test_from_str(self, interval_str: str, expected: Interval) -> None:
        assert Interval.from_str(interval_str) == expected

    def test_from_str_invalid_raises_parse_error(self) -> None:
        with pytest.raises(ParseError, match="Invalid interval: X9"):
            Interval.from_str("X9")

    @pytest.mark.parametrize("interval", list(Interval))
    def test_to_str_from_str_round_trip(self, interval: Interval) -> None:
        assert Interval.from_str(interval.to_str()) == interval

    @pytest.mark.parametrize(
        ("interval", "expected"),
        [
            (Interval.Unison, 0),
            (Interval.MinorSecond, 1),
            (Interval.PerfectFifth, 7),
            (Interval.Octave, 12),
            (Interval.MajorThirteenth, 21),
        ],
    )
    def test_to_int(self, interval: Interval, expected: int) -> None:
        assert interval.to_int() == expected

    def test_from_int_invalid_raises_parse_error(self) -> None:
        with pytest.raises(ParseError, match="Invalid interval: 22"):
            Interval.from_int(22)

    @pytest.mark.parametrize("interval", list(Interval))
    def test_to_int_from_int_round_trip(self, interval: Interval) -> None:
        assert Interval.from_int(interval.to_int()) == interval
