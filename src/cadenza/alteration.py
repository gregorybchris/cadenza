import logging
from enum import StrEnum, auto

from cadenza.utils.symbol_utils import remove_symbols

logger = logging.getLogger(__name__)


class Alteration(StrEnum):
    FlatFive = auto()

    @classmethod
    def from_str(cls, alteration_str: str) -> "Alteration":
        alteration_str = remove_symbols(alteration_str)
        match alteration_str:
            case "b5":
                return cls.FlatFive

        msg = f"Invalid alteration: {alteration_str}"
        raise ValueError(msg)

    def to_str(self, symbols: bool = True) -> str:
        match self:
            case Alteration.FlatFive:
                return "♭5" if symbols else "b5"

    def __str__(self) -> str:
        return self.to_str()

    def __repr__(self) -> str:
        return self.value
