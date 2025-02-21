import logging
from enum import StrEnum, auto

logger = logging.getLogger(__name__)


class Inversion(StrEnum):
    Root = auto()
    First = auto()
    Second = auto()
    Third = auto()

    def to_number(self) -> int:
        return {
            Inversion.Root: 0,
            Inversion.First: 1,
            Inversion.Second: 2,
            Inversion.Third: 3,
        }[self]

    @classmethod
    def from_number(cls, number: int) -> "Inversion":
        return {
            0: Inversion.Root,
            1: Inversion.First,
            2: Inversion.Second,
            3: Inversion.Third,
        }[number]

    def to_written(self) -> str:
        return {
            Inversion.Root: "root position",
            Inversion.First: "first inversion",
            Inversion.Second: "second inversion",
            Inversion.Third: "third inversion",
        }[self]
