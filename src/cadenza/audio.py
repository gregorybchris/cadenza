from dataclasses import dataclass
from pathlib import Path

import sounddevice
import torch
import torchaudio
from torch import Tensor

from cadenza.chord import Chord
from cadenza.note import Note


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

    def generate_silence(self, duration: float) -> Tensor:
        return torch.zeros(int(self.args.sample_rate * duration), dtype=torch.float32)

    def generate(self, frequencies: Tensor, duration: float) -> Tensor:
        # Time vector
        t = torch.linspace(0, duration, int(self.args.sample_rate * duration), dtype=torch.float32)

        # Generate sine waves
        amplitude = 0.5
        tones = torch.stack([amplitude * torch.sin(2 * torch.pi * f * t) for f in frequencies])

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

    def concat(self, segments: list[Tensor]) -> Tensor:
        return torch.cat(segments)


def get_frequency(reference_frequency: float, intervals: Tensor) -> Tensor:
    return reference_frequency * 2 ** (intervals / 12)


def generate_chord_audio(chord: Chord, reference_note: Note, reference_frequency: float, synth: Synth) -> Tensor:
    intervals = torch.tensor([interval.to_int() for interval in chord.to_intervals()])
    scale_degree = chord.root.to_index() - reference_note.to_index()
    intervals += scale_degree  # Transpose
    frequencies = get_frequency(reference_frequency, intervals)
    return synth.generate(frequencies, 0.8)


if __name__ == "__main__":
    sample_rate = 44_100

    synth_args = SynthArgs(sample_rate=sample_rate)
    synth = Synth(args=synth_args)

    reference_note = Note.from_str("A")
    reference_frequency = 440.0  # A4

    chord_strs = ["A", "E", "F#m", "D", "A"]
    segments: list[Tensor] = []
    for chord_str in chord_strs:
        chord = Chord.from_str(chord_str)
        segment = generate_chord_audio(chord, reference_note, reference_frequency, synth)
        segments.append(segment)

        audio_silence = synth.generate_silence(0.1)
        segments.append(audio_silence)

    audio = synth.concat(segments)

    player = Player(sample_rate=sample_rate)
    player.play(audio)

    saver = Saver(sample_rate=sample_rate)
    audio_filepath = Path("data/output.wav")
    saver.save(audio, audio_filepath)
