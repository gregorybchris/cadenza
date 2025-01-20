import logging
from enum import StrEnum, auto

from cadenza.errors import ParseError
from cadenza.utils.symbol_utils import remove_symbols

logger = logging.getLogger(__name__)


class Alteration(StrEnum):
    FlatFive = auto()
    FlatNine = auto()

    @classmethod
    def from_str(cls, alteration_str: str) -> "Alteration":
        alteration_str = remove_symbols(alteration_str)
        mapping = {
            "b5": cls.FlatFive,
            "b9": cls.FlatNine,
        }
        if alteration_str not in mapping:
            msg = f"Invalid extension: {alteration_str}"
            raise ParseError(msg)
        return mapping[alteration_str]

    def to_str(self, symbols: bool = True) -> str:
        match self:
            case Alteration.FlatFive:
                return "♭5" if symbols else "b5"
            case Alteration.FlatNine:
                return "♭9" if symbols else "b9"

    def __str__(self) -> str:
        return self.to_str()

    def __repr__(self) -> str:
        return self.value
