import pytest

from cadenza import Interval, ScaleDegree


class TestScaleDegree:
    @pytest.mark.parametrize(
        ("scale_degree", "expected"),
        [
            (ScaleDegree.Tonic, "tonic"),
            (ScaleDegree.Supertonic, "supertonic"),
            (ScaleDegree.Mediant, "mediant"),
            (ScaleDegree.Subdominant, "subdominant"),
            (ScaleDegree.Dominant, "dominant"),
            (ScaleDegree.Submediant, "submediant"),
            (ScaleDegree.LeadingTone, "leading tone"),
        ],
    )
    def test_to_written(self, scale_degree: ScaleDegree, expected: str) -> None:
        assert scale_degree.to_written() == expected

    @pytest.mark.parametrize(
        ("scale_degree", "expected"),
        [
            (ScaleDegree.Tonic, "I"),
            (ScaleDegree.Supertonic, "II"),
            (ScaleDegree.Mediant, "III"),
            (ScaleDegree.Subdominant, "IV"),
            (ScaleDegree.Dominant, "V"),
            (ScaleDegree.Submediant, "VI"),
            (ScaleDegree.LeadingTone, "VII"),
        ],
    )
    def test_to_symbol(self, scale_degree: ScaleDegree, expected: str) -> None:
        assert scale_degree.to_symbol() == expected

    @pytest.mark.parametrize(
        ("degree", "expected"),
        [
            (0, ScaleDegree.Tonic),
            (4, ScaleDegree.Dominant),
            (6, ScaleDegree.LeadingTone),
            (7, ScaleDegree.Tonic),
            (-1, ScaleDegree.LeadingTone),
        ],
    )
    def test_from_int(self, degree: int, expected: ScaleDegree) -> None:
        assert ScaleDegree.from_int(degree) == expected

    @pytest.mark.parametrize("scale_degree", list(ScaleDegree))
    def test_to_int_from_int_round_trip(self, scale_degree: ScaleDegree) -> None:
        assert ScaleDegree.from_int(scale_degree.to_int()) == scale_degree

    @pytest.mark.parametrize(
        ("interval", "expected"),
        [
            (Interval.Unison, ScaleDegree.Tonic),
            (Interval.MajorSecond, ScaleDegree.Supertonic),
            (Interval.MinorThird, ScaleDegree.Mediant),
            (Interval.MajorThird, ScaleDegree.Mediant),
            (Interval.PerfectFourth, ScaleDegree.Subdominant),
            (Interval.PerfectFifth, ScaleDegree.Dominant),
            (Interval.MinorSixth, ScaleDegree.Submediant),
            (Interval.MajorSixth, ScaleDegree.Submediant),
            (Interval.MinorSeventh, ScaleDegree.LeadingTone),
            (Interval.MajorSeventh, ScaleDegree.LeadingTone),
            (Interval.Octave, ScaleDegree.Tonic),
        ],
    )
    def test_from_interval(self, interval: Interval, expected: ScaleDegree) -> None:
        assert ScaleDegree.from_interval(interval) == expected

    @pytest.mark.parametrize(
        ("interval", "expected_msg"),
        [
            (Interval.MinorSecond, "Minor second is not a valid interval for scale degrees"),
            (Interval.Tritone, "Tritone is not a valid interval for scale degrees"),
            (Interval.MajorNinth, "Major ninth is not a valid interval for scale degrees"),
        ],
    )
    def test_from_interval_invalid_raises_value_error(self, interval: Interval, expected_msg: str) -> None:
        with pytest.raises(ValueError, match=expected_msg):
            ScaleDegree.from_interval(interval)

    @pytest.mark.parametrize("scale_degree", list(ScaleDegree))
    def test_from_str(self, scale_degree: ScaleDegree) -> None:
        assert ScaleDegree.from_str(scale_degree.name) == scale_degree
