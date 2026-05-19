import logging
from enum import StrEnum, auto

logger = logging.getLogger(__name__)


class Accidental(StrEnum):
    Sharp = auto()
    Flat = auto()
