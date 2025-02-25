import logging
from enum import StrEnum, auto

from cadenza.constants import (
    AUG_CHARS,
    AUG_SYMBOL,
    DIM_CHARS,
    DIM_SYMBOL,
    HALFDIM_CHARS,
    HALFDIM_SYMBOL,
    MAJ_CHARS,
    MAJ_SYMBOL,
    MIN_CHARS,
    MIN_SYMBOL,
)
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

    def is_suffix(self) -> bool:
        return self in [Quality.SusTwo, Quality.SusFour]

    def is_prefix(self) -> bool:
        return not self.is_suffix()

    @classmethod
    def from_str(cls, quality_str: str) -> "Quality":
        quality_str = remove_symbols(quality_str)
        mapping = {
            MAJ_CHARS: cls.Major,
            MIN_CHARS: cls.Minor,
            DIM_CHARS: cls.Diminished,
            AUG_CHARS: cls.Augmented,
            HALFDIM_CHARS: cls.HalfDiminished,
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
                return MAJ_SYMBOL if symbols else MAJ_CHARS
            case Quality.Minor:
                return MIN_SYMBOL if symbols else MIN_CHARS
            case Quality.Diminished:
                return DIM_SYMBOL if symbols else DIM_CHARS
            case Quality.Augmented:
                return AUG_SYMBOL if symbols else AUG_CHARS
            case Quality.HalfDiminished:
                return HALFDIM_SYMBOL if symbols else HALFDIM_CHARS
            case Quality.SusTwo:
                return "sus2"
            case Quality.SusFour:
                return "sus4"

    def __str__(self) -> str:
        return self.to_str()

    def __repr__(self) -> str:
        return self.value
