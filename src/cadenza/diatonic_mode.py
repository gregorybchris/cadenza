import logging
from enum import StrEnum, auto

logger = logging.getLogger(__name__)


class DiatonicMode(StrEnum):
    Ionian = auto()  # Major
    Dorian = auto()
    Phrygian = auto()
    Lydian = auto()
    Mixolydian = auto()
    Aeolian = auto()  # Natural Minor
    Locrian = auto()

    def to_written(self) -> str:  # noqa: PLR0911
        match self:
            case DiatonicMode.Ionian:
                return "ionian"
            case DiatonicMode.Dorian:
                return "dorian"
            case DiatonicMode.Phrygian:
                return "phrygian"
            case DiatonicMode.Lydian:
                return "lydian"
            case DiatonicMode.Mixolydian:
                return "mixolydian"
            case DiatonicMode.Aeolian:
                return "aeolian"
            case DiatonicMode.Locrian:
                return "locrian"

    @classmethod
    def from_str(cls, mode_str: str) -> "DiatonicMode":  # noqa: PLR0911
        match mode_str:
            case "ionian":
                return cls.Ionian
            case "dorian":
                return cls.Dorian
            case "phrygian":
                return cls.Phrygian
            case "lydian":
                return cls.Lydian
            case "mixolydian":
                return cls.Mixolydian
            case "aeolian":
                return cls.Aeolian
            case "locrian":
                return cls.Locrian

        msg = f"Invalid mode: {mode_str}"
        raise ValueError(msg)

    def __str__(self) -> str:
        return self.to_written()

    def __repr__(self) -> str:
        return self.value
