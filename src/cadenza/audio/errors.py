"""Dependency guard for the optional ``[audio]`` extra."""

import importlib.util

_AUDIO_PACKAGES = ("numpy", "sounddevice", "soundfile", "torch", "torchaudio")


class AudioDependencyError(ImportError):
    """Raised when an audio feature is used without the ``[audio]`` extra installed."""


def require_audio(feature: str) -> None:
    """Raise :class:`AudioDependencyError` if audio dependencies are missing.

    Args:
        feature: Human-readable name of the feature requiring audio support.
    """
    missing = [p for p in _AUDIO_PACKAGES if importlib.util.find_spec(p) is None]
    if missing:
        msg = f'{feature} can be enabled by installing cadenza with `pip install "cadenza[audio]"`'
        raise AudioDependencyError(msg)
