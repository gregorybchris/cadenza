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

    def get_decay(self) -> float:
        match self:
            case OrganPipeLength.TwoFoot:
                return 1 / 9
            case OrganPipeLength.FourFoot:
                return 1 / 4
            case OrganPipeLength.EightFoot:
                return 1
            case OrganPipeLength.SixteenFoot:
                return 1 / 4
            case OrganPipeLength.ThirtyTwoFoot:
                return 1 / 9
            case OrganPipeLength.SixtyFourFoot:
                return 1 / 16
