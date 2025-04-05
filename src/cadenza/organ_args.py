import logging
from dataclasses import dataclass
from typing import Self

from pydantic import BaseModel

from cadenza.organ_pipe_family import OrganPipeFamily
from cadenza.organ_pipe_length import OrganPipeLength

logger = logging.getLogger(__name__)


class OrganStop(BaseModel):
    pipe_family: OrganPipeFamily
    pipe_length: OrganPipeLength

    @classmethod
    def new(cls, pipe_family: OrganPipeFamily, pipe_length: OrganPipeLength) -> Self:
        return cls(pipe_family=pipe_family, pipe_length=pipe_length)


@dataclass(kw_only=True)
class OrganArgs:
    stops: list[OrganStop]

    @classmethod
    def default(cls) -> Self:
        stops = [
            OrganStop.new(OrganPipeFamily.Principals, OrganPipeLength.TwoFoot),
            OrganStop.new(OrganPipeFamily.Principals, OrganPipeLength.FourFoot),
            OrganStop.new(OrganPipeFamily.Principals, OrganPipeLength.EightFoot),
            OrganStop.new(OrganPipeFamily.Principals, OrganPipeLength.SixteenFoot),
            OrganStop.new(OrganPipeFamily.Reeds, OrganPipeLength.EightFoot),
            OrganStop.new(OrganPipeFamily.Flutes, OrganPipeLength.FourFoot),
            OrganStop.new(OrganPipeFamily.Flutes, OrganPipeLength.EightFoot),
            OrganStop.new(OrganPipeFamily.Flutes, OrganPipeLength.SixteenFoot),
            OrganStop.new(OrganPipeFamily.Reeds, OrganPipeLength.EightFoot),
        ]
        return cls(stops=stops)
