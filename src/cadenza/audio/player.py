from dataclasses import dataclass

import sounddevice
from torch import Tensor


@dataclass(kw_only=True)
class Player:
    sample_rate: int

    def play(self, audio: Tensor) -> None:
        sounddevice.play(audio.numpy(), samplerate=self.sample_rate)
        sounddevice.wait()
