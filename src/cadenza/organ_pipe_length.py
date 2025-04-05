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

    @classmethod
    def base(cls) -> "OrganPipeLength":
        return OrganPipeLength.EightFoot

    def get_pitch_multiplier(self) -> float:
        return self.base().get_number() / self.get_number()

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
