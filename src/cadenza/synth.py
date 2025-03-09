from dataclasses import dataclass

import torch
from torch import Tensor

from cadenza.organ_pipe_length import OrganPipeLength


@dataclass(kw_only=True)
class SynthArgs:
    sample_rate: int
    use_tremolo: bool
    use_overtones: bool


@dataclass(kw_only=True)
class Synth:
    args: SynthArgs

    def generate_silence(self, duration_s: float) -> Tensor:
        return torch.zeros(int(self.args.sample_rate * duration_s), dtype=torch.float32)

    def generate(self, frequencies: Tensor, duration_s: float) -> Tensor:
        # Time vector
        t = torch.linspace(0, duration_s, int(self.args.sample_rate * duration_s), dtype=torch.float32)

        # Generate sine waves
        amplitude = 0.5
        tones = torch.stack([amplitude * torch.sin(2 * torch.pi * freq * t) for freq in frequencies])

        # Merge tones by summing them
        audio = tones.sum(dim=0)

        if self.args.use_overtones:
            # Add overtones using organ stops
            for freq in frequencies:
                for pipe_length in OrganPipeLength:
                    multiplier = pipe_length.get_multiplier()
                    overtone_decay = self._get_overtone_decay(pipe_length)
                    overtone = freq * multiplier
                    overtone_amplitude = overtone_decay * amplitude
                    overtone_waveform = overtone_amplitude * torch.sin(2 * torch.pi * overtone * t)
                    audio += overtone_waveform

        # Normalize to prevent clipping
        audio /= len(frequencies)

        if self.args.use_tremolo:
            # Apply tremolo effect
            audio = self._apply_hammond_tremolo(audio)

        return audio

    def _get_overtone_decay(self, pipe_length: OrganPipeLength) -> float:
        match pipe_length:
            case OrganPipeLength.TwoFoot:
                return 1 / 9
            case OrganPipeLength.FourFoot:
                return 1 / 4
            case OrganPipeLength.EightFoot:
                return 1
            case OrganPipeLength.SixteenFoot:
                return 1 / 4
            case OrganPipeLength.ThirtyTwoFoot:
                return 1 / 9
            case OrganPipeLength.SixtyFourFoot:
                return 1 / 16

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

    def _apply_tremolo(self, audio: Tensor, *, frequency: float, dip: float) -> Tensor:
        sample_rate = self.args.sample_rate
        audio_duration = len(audio) / sample_rate

        t = torch.linspace(0, audio_duration, len(audio), dtype=torch.float32)
        height = 1.0 - dip
        amplitude = dip + height * torch.sin(2 * torch.pi * frequency * t)
        return audio * amplitude

    def _apply_hammond_tremolo(self, audio: Tensor) -> Tensor:
        # Apply high frequency tremolo
        audio = self._apply_tremolo(audio, frequency=5.2, dip=0.92)

        # Apply low frequency tremolo, like the Leslie effect on a Hammond organ
        audio = self._apply_tremolo(audio, frequency=1.7, dip=0.92)

        return audio  # noqa: RET504
