import logging

from pydantic import BaseModel

from cadenza.organ_pipe_length import OrganPipeLength
from cadenza.organ_pipe_type import OrganPipeType

logger = logging.getLogger(__name__)


class OrganStop(BaseModel):
    pipe_length: OrganPipeLength
    pipe_type: OrganPipeType
