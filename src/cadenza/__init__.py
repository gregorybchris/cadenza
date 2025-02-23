import importlib.metadata

from cadenza.alteration import Alteration
from cadenza.chord import Chord
from cadenza.composer import Composer
from cadenza.diatonic_mode import DiatonicMode
from cadenza.diatonic_scale import DiatonicScale
from cadenza.extension import Extension
from cadenza.functional_analysis import FunctionalAnalysis
from cadenza.interval import Interval
from cadenza.inversion import Inversion
from cadenza.note import Note
from cadenza.pitch import Pitch
from cadenza.quality import Quality
from cadenza.transposer import Transposer
from cadenza.voicing import Voicing

__version__ = importlib.metadata.version("cadenza")

__all__ = [
    "Alteration",
    "Chord",
    "Composer",
    "DiatonicMode",
    "DiatonicScale",
    "Extension",
    "FunctionalAnalysis",
    "Interval",
    "Inversion",
    "Note",
    "Pitch",
    "Quality",
    "Transposer",
    "Voicing",
    "__version__",
]
