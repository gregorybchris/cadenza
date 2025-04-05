import logging
from dataclasses import dataclass
from typing import Self

from pydantic import BaseModel

from cadenza.organ_pipe_family import OrganPipeFamily
from cadenza.organ_pipe_length import OrganPipeLength

logger = logging.getLogger(__name__)


class OrganStop(BaseModel):
    pipe_length: OrganPipeLength
    pipe_family: OrganPipeFamily


@dataclass(kw_only=True)
class OrganArgs:
    stops: list[OrganStop]

    @classmethod
    def default(cls) -> Self:
        stops = [
            OrganStop(pipe_family=OrganPipeFamily.Principals, pipe_length=OrganPipeLength.TwoFoot),
            OrganStop(pipe_family=OrganPipeFamily.Principals, pipe_length=OrganPipeLength.FourFoot),
            OrganStop(pipe_family=OrganPipeFamily.Principals, pipe_length=OrganPipeLength.EightFoot),
            OrganStop(pipe_family=OrganPipeFamily.Principals, pipe_length=OrganPipeLength.SixteenFoot),
            OrganStop(pipe_family=OrganPipeFamily.Reeds, pipe_length=OrganPipeLength.EightFoot),
            OrganStop(pipe_family=OrganPipeFamily.Flutes, pipe_length=OrganPipeLength.FourFoot),
            OrganStop(pipe_family=OrganPipeFamily.Flutes, pipe_length=OrganPipeLength.EightFoot),
            OrganStop(pipe_family=OrganPipeFamily.Flutes, pipe_length=OrganPipeLength.SixteenFoot),
            OrganStop(pipe_family=OrganPipeFamily.Reeds, pipe_length=OrganPipeLength.EightFoot),
        ]
        return cls(stops=stops)
