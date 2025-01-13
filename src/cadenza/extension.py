import logging
from enum import StrEnum, auto

from cadenza.errors import ParseError

logger = logging.getLogger(__name__)


class Extension(StrEnum):
    Seven = auto()
    MajorSeven = auto()
    AddNine = auto()
    AddEleven = auto()
    AddThirteen = auto()

    @classmethod
    def from_str(cls, extension_str: str) -> "Extension":
        mapping = {
            "7": cls.Seven,
            "maj7": cls.MajorSeven,
            "add9": cls.AddNine,
            "9": cls.AddNine,
            "add11": cls.AddEleven,
            "11": cls.AddEleven,
            "add13": cls.AddThirteen,
            "13": cls.AddThirteen,
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
            case Extension.AddNine:
                return "add9"
            case Extension.AddEleven:
                return "add11"
            case Extension.AddThirteen:
                return "add13"

    def __str__(self) -> str:
        return self.to_str()

    def __repr__(self) -> str:
        return str(self)
