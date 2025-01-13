import logging
from enum import StrEnum, auto

from cadenza.errors import ParseError
from cadenza.utils.symbol_utils import remove_symbols

logger = logging.getLogger(__name__)


class Quality(StrEnum):
    Major = auto()
    Minor = auto()
    Diminished = auto()
    Augmented = auto()
    HalfDiminished = auto()
    SusTwo = auto()
    SusFour = auto()

    def to_written(self) -> str:  # noqa: PLR0911
        match self:
            case Quality.Major:
                return "major"
            case Quality.Minor:
                return "minor"
            case Quality.Diminished:
                return "diminished"
            case Quality.Augmented:
                return "augmented"
            case Quality.HalfDiminished:
                return "half-diminished"
            case Quality.SusTwo:
                return "suspended second"
            case Quality.SusFour:
                return "suspended fourth"

    @classmethod
    def from_str(cls, quality_str: str) -> "Quality":
        quality_str = remove_symbols(quality_str)
        mapping = {
            "": cls.Major,
            "m": cls.Minor,
            "dim": cls.Diminished,
            "aug": cls.Augmented,
            "halfdim": cls.HalfDiminished,
            "sus2": cls.SusTwo,
            "sus4": cls.SusFour,
        }
        if quality_str not in mapping:
            msg = f"Invalid quality: {quality_str}"
            raise ParseError(msg)
        return mapping[quality_str]

    def to_str(self, symbols: bool = True) -> str:  # noqa: PLR0911
        match self:
            case Quality.Major:
                return ""
            case Quality.Minor:
                return "m"
            case Quality.Diminished:
                return "dim"
            case Quality.Augmented:
                return "+" if symbols else "aug"
            case Quality.HalfDiminished:
                return "ø" if symbols else "halfdim"
            case Quality.SusTwo:
                return "sus2"
            case Quality.SusFour:
                return "sus4"

    def __str__(self) -> str:
        return self.to_str()

    def __repr__(self) -> str:
        return self.value
