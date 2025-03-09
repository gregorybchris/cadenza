from dataclasses import dataclass
from typing import Optional


@dataclass(kw_only=True)
class Envelope:
    attack: float = 0.1
    decay: float = 0.15
    sustain: Optional[float] = None
    release: float = 0.1

    sustain_level: float = 0.8
