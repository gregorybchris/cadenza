from dataclasses import dataclass

import torch
from torch import Tensor

from cadenza.voicing import Voicing


@dataclass(kw_only=True)
class SynthArgs:
    sample_rate: int


@dataclass(kw_only=True)
class Synth:
    args: SynthArgs

    def generate_silence(self, duration_s: float) -> Tensor:
        return torch.zeros(int(self.args.sample_rate * duration_s), dtype=torch.float32)

    def generate(self, frequencies: Tensor, duration_s: float, overtones: bool = False) -> Tensor:
        # Time vector
        t = torch.linspace(0, duration_s, int(self.args.sample_rate * duration_s), dtype=torch.float32)

        # Generate sine waves
        amplitude = 0.5
        tones = torch.stack([amplitude * torch.sin(2 * torch.pi * f * t) for f in frequencies])

        # Merge tones by summing them
        audio = tones.sum(dim=0)

        if overtones:
            # Add overtones with exponential decay
            for freq in frequencies:
                for i in range(2, 10):
                    overtone = freq * i
                    decay = 1 / i**2
                    overtone_amplitude = decay * amplitude
                    overtone_waveform = overtone_amplitude * torch.sin(2 * torch.pi * overtone * t)
                    audio += overtone_waveform

        # Normalize to prevent clipping
        audio /= len(frequencies)
        return audio

    def concat(self, segments: list[Tensor]) -> Tensor:
        return torch.cat(segments)

    def generate_voicing_audio(
        self,
        voicing: Voicing,
        duration_s: float,
        overtones: bool = False,
    ) -> Tensor:
        pitches = voicing.get_pitches()
        frequencies = torch.tensor([pitch.get_frequency() for pitch in pitches])
        return self.generate(frequencies, duration_s, overtones=overtones)
