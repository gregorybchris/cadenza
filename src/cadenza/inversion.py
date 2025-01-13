import logging
from enum import StrEnum, auto

logger = logging.getLogger(__name__)


class Inversion(StrEnum):
    Root = auto()
    First = auto()
    Second = auto()
    Third = auto()
