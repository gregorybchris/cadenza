import logging
from enum import StrEnum, auto

logger = logging.getLogger(__name__)


class OrganPipeFamily(StrEnum):
    Flutes = auto()
    Principals = auto()
    Reeds = auto()
    Strings = auto()
