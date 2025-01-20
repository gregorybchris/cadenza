from dataclasses import dataclass

import torch
from torch import Tensor

from cadenza.organ_stop import OrganStop
from cadenza.pitch import Pitch
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
        tones = torch.stack([amplitude * torch.sin(2 * torch.pi * freq * t) for freq in frequencies])

        # Merge tones by summing them
        audio = tones.sum(dim=0)

        if overtones:
            # Add overtones using organ stops
            for freq in frequencies:
                for stop in OrganStop:
                    multiplier = stop.get_multiplier()
                    decay = stop.get_decay()
                    overtone = freq * multiplier
                    overtone_amplitude = decay * amplitude
                    overtone_waveform = overtone_amplitude * torch.sin(2 * torch.pi * overtone * t)
                    audio += overtone_waveform

        # Normalize to prevent clipping
        audio /= len(frequencies)
        return audio

    def concat(self, segments: list[Tensor]) -> Tensor:
        return torch.cat(segments)

    def generate_pitch_audio(
        self,
        pitch: Pitch,
        duration_s: float,
        overtones: bool = False,
    ) -> Tensor:
        frequency = pitch.get_frequency()
        frequencies = torch.tensor([frequency])
        return self.generate(frequencies, duration_s, overtones=overtones)

    def generate_voicing_audio(
        self,
        voicing: Voicing,
        duration_s: float,
        overtones: bool = False,
    ) -> Tensor:
        pitches = voicing.get_pitches()
        frequencies = torch.tensor([pitch.get_frequency() for pitch in pitches])
        return self.generate(frequencies, duration_s, overtones=overtones)

    def apply_tremolo(self, audio: Tensor, *, frequency: float, dip: float) -> Tensor:
        sample_rate = self.args.sample_rate
        audio_duration = len(audio) / sample_rate

        t = torch.linspace(0, audio_duration, len(audio), dtype=torch.float32)
        height = 1.0 - dip
        amplitude = dip + height * torch.sin(2 * torch.pi * frequency * t)
        return audio * amplitude

    def apply_hammond_tremolo(self, audio: Tensor) -> Tensor:
        # Apply high frequency tremolo
        audio = self.apply_tremolo(audio, frequency=5.2, dip=0.92)

        # Apply low frequency tremolo, like the Leslie effect on a Hammond organ
        audio = self.apply_tremolo(audio, frequency=1.7, dip=0.92)

        return audio  # noqa: RET504
