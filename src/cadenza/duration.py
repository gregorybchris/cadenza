from enum import StrEnum, auto


class Duration(StrEnum):
    Whole = auto()
    Half = auto()
    Quarter = auto()
    Eighth = auto()
    Sixteenth = auto()
    ThirtySecond = auto()

    def get_n_quarter_notes(self) -> float:
        return {
            Duration.Whole: 4.0,
            Duration.Half: 2.0,
            Duration.Quarter: 1.0,
            Duration.Eighth: 0.5,
            Duration.Sixteenth: 0.25,
            Duration.ThirtySecond: 0.125,
        }[self]
