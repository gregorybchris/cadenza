from dataclasses import dataclass
from typing import Self


@dataclass(kw_only=True)
class Tremolo:
    frequency: float
    dip: float


@dataclass(kw_only=True)
class TremoloArgs:
    tremolos: list[Tremolo]

    @classmethod
    def hammond(cls) -> Self:
        high_frequency = Tremolo(frequency=5.2, dip=0.92)
        low_frequency = Tremolo(frequency=1.7, dip=0.92)
        return cls(tremolos=[high_frequency, low_frequency])
