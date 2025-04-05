from dataclasses import dataclass, field
from typing import Optional

import torch
import torch.fft
from torch import Tensor

from cadenza.envelope import Envelope
from cadenza.organ_args import OrganArgs
from cadenza.organ_pipe_family import OrganPipeFamily
from cadenza.reverb_model import ReverbModel
from cadenza.tremolo_args import Tremolo, TremoloArgs


@dataclass(kw_only=True)
class SynthArgs:
    sample_rate: int
    tremolo_args: Optional[TremoloArgs] = None
    organ_args: Optional[OrganArgs] = None
    lowpass_cutoff: Optional[float] = None
    highpass_cutoff: Optional[float] = None
    envelope: Optional[Envelope] = field(default_factory=Envelope)


@dataclass(kw_only=True)
class Synth:
    args: SynthArgs

    def generate_silence(self, duration_s: float) -> Tensor:
        return torch.zeros(int(self.args.sample_rate * duration_s), dtype=torch.float32)

    def generate(self, frequencies: Tensor, duration_s: float) -> Tensor:
        # Time vector
        time_tensor = torch.linspace(0, duration_s, int(self.args.sample_rate * duration_s), dtype=torch.float32)

        # Generate sine waves
        amplitude = 0.5
        tones = torch.stack([amplitude * torch.sin(2 * torch.pi * freq * time_tensor) for freq in frequencies])

        # Merge tones by summing them
        audio = tones.sum(dim=0)

        if self.args.organ_args:
            # Add overtones using organ stops
            audio = self._apply_overtones(audio, self.args.organ_args, frequencies, amplitude, time_tensor)

        if self.args.tremolo_args:
            # Apply tremolo effect
            audio = self._apply_tremolos(audio, self.args.tremolo_args)

        # Apply ADSR envelope
        if self.args.envelope is not None:
            audio = self._apply_envelope(audio, self.args.envelope)

        # Apply band-pass filter
        audio = self._apply_bandpass_filter(audio, self.args.lowpass_cutoff, self.args.highpass_cutoff)

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

    def _apply_overtones(
        self,
        audio: Tensor,
        organ_args: OrganArgs,
        played_frequencies: Tensor,
        amplitude: float,
        time_tensor: Tensor,
    ) -> Tensor:
        for played_frequency in played_frequencies:
            for stop in organ_args.stops:
                pipe_length_multiplier = stop.pipe_length.get_pitch_multiplier()
                fundamental = played_frequency * pipe_length_multiplier
                overtone_amplitudes = self._get_overtone_amplitudes(stop.pipe_family)
                for overtone_number, overtone_amplitude in enumerate(overtone_amplitudes):
                    overtone_multiplier = overtone_number + 1
                    overtone_frequency = fundamental * overtone_multiplier
                    audio += amplitude * overtone_amplitude * torch.sin(2 * torch.pi * overtone_frequency * time_tensor)
        return audio

    def _get_overtone_amplitudes(self, pipe_family: OrganPipeFamily) -> list[float]:
        match pipe_family:
            case OrganPipeFamily.Strings:
                return [0.70, 0.20, 0.20, 0.1, 0.06, 0.04, 0.03, 0.02, 0.01]
            case OrganPipeFamily.Flutes:
                return [0.70, 0.02, 0.01]
            case OrganPipeFamily.Principals:
                return [0.90, 0.50, 0.20, 0.10, 0.05]
            case OrganPipeFamily.Reeds:
                return [0.50, 0.2, 0.1, 0.08, 0.03]

    def _apply_tremolos(self, audio: Tensor, tremolo_args: TremoloArgs) -> Tensor:
        for tremolo in tremolo_args.tremolos:
            audio = self._apply_tremolo(audio, tremolo)
        return audio

    def _apply_tremolo(self, audio: Tensor, tremolo: Tremolo) -> Tensor:
        sample_rate = self.args.sample_rate
        audio_duration = len(audio) / sample_rate

        t = torch.linspace(0, audio_duration, len(audio), dtype=torch.float32)
        height = 1.0 - tremolo.dip
        amplitude = tremolo.dip + height * torch.sin(2 * torch.pi * tremolo.frequency * t)
        return audio * amplitude

    def _apply_envelope(self, audio: Tensor, envelope: Envelope) -> Tensor:
        duration_s = len(audio) / self.args.sample_rate
        sustain = envelope.sustain
        if sustain is None:
            sustain = duration_s - envelope.attack - envelope.decay - envelope.release

        n_a = int(envelope.attack * self.args.sample_rate)
        n_d = int(envelope.decay * self.args.sample_rate)
        n_s = int(sustain * self.args.sample_rate)
        n_r = int(envelope.release * self.args.sample_rate)

        n_ad = n_a + n_d
        n_ads = n_ad + n_s
        n_adsr = n_ads + n_r

        envelope_mask = torch.zeros_like(audio)
        envelope_mask[:n_a] = torch.linspace(0, 1, n_a)
        envelope_mask[n_a:n_ad] = torch.linspace(1, envelope.sustain_level, n_d)
        envelope_mask[n_ad:n_ads] = envelope.sustain_level
        envelope_mask[n_ads:n_adsr] = torch.linspace(envelope.sustain_level, 0, n_r)

        return audio * envelope_mask

    def _apply_bandpass_filter(
        self,
        audio: Tensor,
        lowpass_cutoff: Optional[float],
        highpass_cutoff: Optional[float],
    ) -> Tensor:
        freqs = torch.fft.fftfreq(audio.shape[0], d=1 / 16000)
        mask = torch.ones_like(freqs, dtype=torch.bool)
        abs_freqs = torch.abs(freqs)
        if lowpass_cutoff is not None:
            mask &= abs_freqs <= lowpass_cutoff
        if highpass_cutoff is not None:
            mask &= abs_freqs >= highpass_cutoff

        fft_audio = torch.fft.fft(audio)
        fft_filtered = fft_audio * mask
        return torch.fft.ifft(fft_filtered).real

    def apply_cathedral_reverb(self, audio: Tensor) -> Tensor:
        return self.apply_reverb(audio, delay_s=0.3, feedback=0.5)

    def apply_reverb(self, audio: Tensor, delay_s: float, feedback: float) -> Tensor:
        delay_samples = int(self.args.sample_rate * delay_s)
        model = ReverbModel(delay_samples=delay_samples, feedback=feedback)
        return model(audio)
