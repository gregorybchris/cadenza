from dataclasses import dataclass
from pathlib import Path

import torchaudio
from torch import Tensor


@dataclass(kw_only=True)
class Saver:
    sample_rate: int

    def save(self, audio: Tensor, filepath: Path) -> None:
        audio_tensor = audio.unsqueeze(0)  # Convert to 2D tensor (1 channel)
        torchaudio.save(str(filepath), audio_tensor, self.sample_rate)
