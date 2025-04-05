import logging
from enum import StrEnum, auto

logger = logging.getLogger(__name__)


class OrganPipeFamily(StrEnum):
    Strings = auto()
    Principals = auto()
    Flutes = auto()
    Reeds = auto()
