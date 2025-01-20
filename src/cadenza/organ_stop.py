import logging
from enum import StrEnum, auto

logger = logging.getLogger(__name__)


class OrganStop(StrEnum):
    OneFoot = auto()
    TwoFoot = auto()
    FourFoot = auto()
    EightFoot = auto()
    SixteenFoot = auto()
    ThirtyTwoFoot = auto()

    def get_multiplier(self) -> float:
        match self:
            case OrganStop.OneFoot:
                return 1 / 8
            case OrganStop.TwoFoot:
                return 1 / 4
            case OrganStop.FourFoot:
                return 1 / 2
            case OrganStop.EightFoot:
                return 1
            case OrganStop.SixteenFoot:
                return 2
            case OrganStop.ThirtyTwoFoot:
                return 4

    def get_decay(self) -> float:
        match self:
            case OrganStop.OneFoot:
                return 1 / 16
            case OrganStop.TwoFoot:
                return 1 / 9
            case OrganStop.FourFoot:
                return 1 / 4
            case OrganStop.EightFoot:
                return 1
            case OrganStop.SixteenFoot:
                return 1 / 4
            case OrganStop.ThirtyTwoFoot:
                return 1 / 9
