import importlib.metadata

from cadenza.alteration import Alteration
from cadenza.chord import Chord
from cadenza.diatonic_mode import DiatonicMode
from cadenza.extension import Extension
from cadenza.interval import Interval
from cadenza.inversion import Inversion
from cadenza.note import Note
from cadenza.quality import Quality

__version__ = importlib.metadata.version("cadenza")

__all__ = [
    "Alteration",
    "Chord",
    "DiatonicMode",
    "Extension",
    "Interval",
    "Inversion",
    "Note",
    "Quality",
    "__version__",
]
