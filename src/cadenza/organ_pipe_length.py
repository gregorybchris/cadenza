import logging
from enum import StrEnum, auto

logger = logging.getLogger(__name__)


class OrganPipeLength(StrEnum):
    TwoFoot = auto()
    FourFoot = auto()
    EightFoot = auto()
    SixteenFoot = auto()
    ThirtyTwoFoot = auto()
    SixtyFourFoot = auto()

    def get_multiplier(self) -> float:
        match self:
            case OrganPipeLength.TwoFoot:
                return 1 / 3
            case OrganPipeLength.FourFoot:
                return 1 / 2
            case OrganPipeLength.EightFoot:
                return 1
            case OrganPipeLength.SixteenFoot:
                return 2
            case OrganPipeLength.ThirtyTwoFoot:
                return 3
            case OrganPipeLength.SixtyFourFoot:
                return 4

    def get_number(self) -> int:
        match self:
            case OrganPipeLength.TwoFoot:
                return 2
            case OrganPipeLength.FourFoot:
                return 4
            case OrganPipeLength.EightFoot:
                return 8
            case OrganPipeLength.SixteenFoot:
                return 16
            case OrganPipeLength.ThirtyTwoFoot:
                return 32
            case OrganPipeLength.SixtyFourFoot:
                return 64
