from dataclasses import dataclass
from typing import Optional

from torch import Tensor
from torchaudio.transforms import AmplitudeToDB, MelSpectrogram

try:
    import matplotlib.pyplot as plt

    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


@dataclass(kw_only=True)
class VisualizerArgs:
    sample_rate: int
    n_fft: int = 1024
    win_length: Optional[int] = None
    hop_length: int = 512
    n_mels: int = 128


@dataclass(kw_only=True)
class Visualizer:
    args: VisualizerArgs

    def visualize(self, audio: Tensor) -> None:
        if not HAS_MATPLOTLIB:
            msg = "matplotlib is not installed"
            raise ImportError(msg)

        mel_spectrogram = MelSpectrogram(
            sample_rate=self.args.sample_rate,
            n_fft=self.args.n_fft,
            hop_length=self.args.hop_length,
            n_mels=self.args.n_mels,
        )
        mel_spec = mel_spectrogram(audio)
        amplitude_to_db = AmplitudeToDB()
        mel_spec_db = amplitude_to_db(mel_spec)

        plt.figure(figsize=(10, 4))
        plt.imshow(mel_spec_db.squeeze().numpy(), aspect="auto", origin="lower", cmap="magma")
        plt.colorbar(label="dB")
        plt.xlabel("Time (frames)")
        plt.ylabel("Mel Frequency Bins")
        plt.title("Mel Spectrogram")

        # Force a GUI update to show the plot while the audio is playing
        plt.draw()
        plt.pause(0.1)
