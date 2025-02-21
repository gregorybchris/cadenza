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
        fade_duration_s = 0.05
        sample_rate = self.args.sample_rate
        max_fade_samples = int(fade_duration_s * sample_rate)

        segments = [seg for seg in segments if len(seg) > 0]

        new_segments = [segments[0]]
        for i in range(1, len(segments)):
            seg_a = segments[i - 1]
            seg_b = segments[i]

            # Handle case where segments are shorter than fade duration
            fade_samples = min(max_fade_samples, len(seg_a), len(seg_b))

            fade_out = torch.linspace(1, 0, fade_samples, dtype=torch.float32)
            seg_a[-fade_samples:] *= fade_out

            fade_in = torch.linspace(0, 1, fade_samples, dtype=torch.float32)
            seg_b[:fade_samples] *= fade_in

            new_segments.append(seg_b[fade_samples:])

        return torch.cat(new_segments)

    def generate_pitch_audio(
        self,
        pitch: Pitch,
        duration_s: float,
        overtones: bool = False,
    ) -> Tensor:
        frequency = pitch.to_frequency()
        frequencies = torch.tensor([frequency])
        return self.generate(frequencies, duration_s, overtones=overtones)

    def generate_voicing_audio(
        self,
        voicing: Voicing,
        duration_s: float,
        overtones: bool = False,
    ) -> Tensor:
        pitches = voicing.to_pitches()
        frequencies = torch.tensor([pitch.to_frequency() for pitch in pitches])
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
