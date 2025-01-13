from pathlib import Path

import sounddevice
import torch
import torchaudio
from torch import Tensor


def get_frequency(reference_frequency: float, distance: int) -> float:
    return reference_frequency * 2 ** (distance / 12)


def save_audio(audio: Tensor, filepath: Path, sample_rate: int) -> None:
    audio_tensor = audio.unsqueeze(0)  # Convert to 2D tensor (1 channel)
    torchaudio.save(str(filepath), audio_tensor, sample_rate)


def play_audio(audio: Tensor, sample_rate: int) -> None:
    sounddevice.play(audio.numpy(), samplerate=sample_rate)
    sounddevice.wait()


def generate_audio(frequencies: list[float], duration: float, sample_rate: int) -> Tensor:
    # Time vector
    t = torch.linspace(0, duration, int(sample_rate * duration), dtype=torch.float32)

    # Generate sine waves
    amplitude = 0.5
    tones = torch.stack([amplitude * torch.sin(2 * torch.pi * freq * t) for freq in frequencies])

    # Merge tones by summing them
    combined_waveform = tones.sum(dim=0)

    # Add overtones with exponential decay
    for freq in frequencies:
        for i in range(2, 10):
            overtone = freq * i
            decay = 1 / i**2
            overtone_amplitude = decay * amplitude
            overtone_waveform = overtone_amplitude * torch.sin(2 * torch.pi * overtone * t)
            combined_waveform += overtone_waveform

    # Normalize to prevent clipping
    combined_waveform /= len(frequencies)

    return combined_waveform


if __name__ == "__main__":
    sample_rate = 44100

    duration = 2.0

    reference_frequency = 440.0  # A4

    # Am chord
    frequencies = [
        reference_frequency,  # A4
        get_frequency(reference_frequency, 3),  # C4
        get_frequency(reference_frequency, 7),  # E4
        get_frequency(reference_frequency, 12),  # A5
    ]

    audio = generate_audio(frequencies, duration, sample_rate)
    play_audio(audio, sample_rate)
    audio_filepath = Path("data/output.wav")
    save_audio(audio, audio_filepath, sample_rate)
