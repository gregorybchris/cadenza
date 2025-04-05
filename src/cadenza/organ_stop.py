import logging

from pydantic import BaseModel

from cadenza.organ_pipe_family import OrganPipeFamily
from cadenza.organ_pipe_length import OrganPipeLength

logger = logging.getLogger(__name__)


class OrganStop(BaseModel):
    pipe_length: OrganPipeLength
    pipe_family: OrganPipeFamily
