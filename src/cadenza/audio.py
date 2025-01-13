from dataclasses import dataclass
from pathlib import Path

import sounddevice
import torch
import torchaudio
from torch import Tensor


@dataclass(kw_only=True)
class Saver:
    sample_rate: int

    def save(self, audio: Tensor, filepath: Path) -> None:
        audio_tensor = audio.unsqueeze(0)  # Convert to 2D tensor (1 channel)
        torchaudio.save(str(filepath), audio_tensor, self.sample_rate)


@dataclass(kw_only=True)
class Player:
    sample_rate: int

    def play(self, audio: Tensor) -> None:
        sounddevice.play(audio.numpy(), samplerate=self.sample_rate)
        sounddevice.wait()


@dataclass(kw_only=True)
class SynthArgs:
    sample_rate: int


@dataclass(kw_only=True)
class Synth:
    args: SynthArgs

    def generate(self, frequencies: list[float], duration: float) -> Tensor:
        # Time vector
        t = torch.linspace(0, duration, int(self.args.sample_rate * duration), dtype=torch.float32)

        # Generate sine waves
        amplitude = 0.5
        tones = torch.stack([amplitude * torch.sin(2 * torch.pi * freq * t) for freq in frequencies])

        # Merge tones by summing them
        audio = tones.sum(dim=0)

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


def get_frequency(reference_frequency: float, distance: int) -> float:
    return reference_frequency * 2 ** (distance / 12)


if __name__ == "__main__":
    sample_rate = 44_100

    synth_args = SynthArgs(sample_rate=sample_rate)
    synth = Synth(args=synth_args)

    # Am chord
    reference_frequency = 440.0  # A4
    frequencies = [
        reference_frequency,  # A4
        get_frequency(reference_frequency, 3),  # C4
        get_frequency(reference_frequency, 7),  # E4
        get_frequency(reference_frequency, 12),  # A5
    ]

    duration = 2.0
    audio = synth.generate(frequencies, duration)
    player = Player(sample_rate=sample_rate)
    player.play(audio)

    saver = Saver(sample_rate=sample_rate)
    audio_filepath = Path("data/output.wav")
    saver.save(audio, audio_filepath)
