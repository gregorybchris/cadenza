import logging
from enum import StrEnum, auto

from cadenza.errors import ParseError

logger = logging.getLogger(__name__)


class Extension(StrEnum):
    Seven = auto()
    MajorSeven = auto()
    Nine = auto()
    MajorNine = auto()
    Eleven = auto()
    Thirteen = auto()

    @classmethod
    def from_str(cls, extension_str: str) -> "Extension":
        mapping = {
            "7": cls.Seven,
            "maj7": cls.MajorSeven,
            "9": cls.Nine,
            "maj9": cls.MajorNine,
            "11": cls.Eleven,
            "13": cls.Thirteen,
        }
        if extension_str not in mapping:
            msg = f"Invalid extension: {extension_str}"
            raise ParseError(msg)
        return mapping[extension_str]

    def to_str(self) -> str:
        match self:
            case Extension.Seven:
                return "7"
            case Extension.MajorSeven:
                return "maj7"
            case Extension.Nine:
                return "9"
            case Extension.MajorNine:
                return "maj9"
            case Extension.Eleven:
                return "11"
            case Extension.Thirteen:
                return "13"

    def __str__(self) -> str:
        return self.to_str()

    def __repr__(self) -> str:
        return str(self)
