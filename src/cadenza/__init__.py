import importlib.metadata

from cadenza.core.alteration import Alteration
from cadenza.core.chord import Chord
from cadenza.core.composer import Composer
from cadenza.core.diatonic_mode import DiatonicMode
from cadenza.core.diatonic_scale import DiatonicScale
from cadenza.core.extension import Extension
from cadenza.core.functional_analysis import FunctionalAnalysis
from cadenza.core.interval import Interval
from cadenza.core.inversion import Inversion
from cadenza.core.note import Note
from cadenza.core.note_letter import NoteLetter
from cadenza.core.pitch import Pitch
from cadenza.core.quality import Quality
from cadenza.core.transposer import Transposer
from cadenza.core.voicing import Voicing

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
    "NoteLetter",
    "Pitch",
    "Quality",
    "Transposer",
    "Voicing",
    "__version__",
]
