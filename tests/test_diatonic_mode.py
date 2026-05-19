from cadenza import DiatonicMode, Interval


class TestDiatonicMode:
    def test_get_intervals(self) -> None:
        diatonic_mode = DiatonicMode.Dorian
        intervals = diatonic_mode.get_intervals()
        assert intervals == [
            Interval.Unison,
            Interval.MajorSecond,
            Interval.MinorThird,
            Interval.PerfectFourth,
            Interval.PerfectFifth,
            Interval.MajorSixth,
            Interval.MinorSeventh,
            Interval.Octave,
        ]
