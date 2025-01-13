import logging
from enum import StrEnum, auto

logger = logging.getLogger(__name__)


class Extension(StrEnum):
    Seven = auto()
    MajorSeven = auto()
    AddNine = auto()
    AddEleven = auto()
    AddThirteen = auto()

    @classmethod
    def from_str(cls, extension_str: str) -> "Extension":
        match extension_str:
            case "7":
                return cls.Seven
            case "maj7":
                return cls.MajorSeven
            case "add9":
                return cls.AddNine
            case "add11":
                return cls.AddEleven
            case "add13":
                return cls.AddThirteen

        msg = f"Invalid extension: {extension_str}"
        raise ValueError(msg)

    def to_str(self, symbols: bool = True) -> str:  # noqa: ARG002
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
