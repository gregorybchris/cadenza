from dataclasses import dataclass

import torch
from torch import Tensor

from cadenza.chord import Chord
from cadenza.note import Note


@dataclass(kw_only=True)
class SynthArgs:
    sample_rate: int


@dataclass(kw_only=True)
class Synth:
    args: SynthArgs

    def generate_silence(self, duration: float) -> Tensor:
        return torch.zeros(int(self.args.sample_rate * duration), dtype=torch.float32)

    def generate(self, frequencies: Tensor, duration: float, overtones: bool = False) -> Tensor:
        # Time vector
        t = torch.linspace(0, duration, int(self.args.sample_rate * duration), dtype=torch.float32)

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

    @staticmethod
    def _get_frequency(reference_frequency: float, intervals: Tensor) -> Tensor:
        return reference_frequency * 2 ** (intervals / 12)

    def generate_chord_audio(
        self,
        chord: Chord,
        reference_note: Note,
        reference_frequency: float,
        duration: float,
    ) -> Tensor:
        intervals = torch.tensor([interval.to_int() for interval in chord.to_intervals()])
        scale_degree = chord.root.to_index() - reference_note.to_index()
        intervals += scale_degree  # Transpose
        frequencies = self._get_frequency(reference_frequency, intervals)
        return self.generate(frequencies, duration)
