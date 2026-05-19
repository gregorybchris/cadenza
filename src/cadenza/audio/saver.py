from dataclasses import dataclass
from pathlib import Path

from cadenza.audio.errors import require_audio

try:
    import torchaudio
    from torch import Tensor
except ImportError:
    require_audio("Saving audio to a file")
    raise


@dataclass(kw_only=True)
class Saver:
    sample_rate: int

    def save(self, audio: Tensor, filepath: Path) -> None:
        audio_tensor = audio.unsqueeze(0)  # Convert to 2D tensor (1 channel)
        torchaudio.save(str(filepath), audio_tensor, self.sample_rate)
