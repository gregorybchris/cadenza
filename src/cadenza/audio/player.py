from dataclasses import dataclass

from cadenza.audio.errors import require_audio

try:
    import sounddevice
    from torch import Tensor
except ImportError:
    require_audio("Audio playback")
    raise


@dataclass(kw_only=True)
class Player:
    sample_rate: int

    def play(self, audio: Tensor) -> None:
        sounddevice.play(audio.numpy(), samplerate=self.sample_rate)
        sounddevice.wait()
