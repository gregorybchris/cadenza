import importlib.metadata

from cadenza.core.accidental import Accidental
from cadenza.core.alteration import Alteration
from cadenza.core.chord import Chord
from cadenza.core.composer import Composer
from cadenza.core.diatonic_key import DiatonicKey
from cadenza.core.diatonic_mode import DiatonicMode
from cadenza.core.diatonic_scale import DiatonicScale
from cadenza.core.duration import Duration
from cadenza.core.envelope import Envelope
from cadenza.core.errors import ParseError
from cadenza.core.extension import Extension
from cadenza.core.functional_analysis import FunctionalAnalysis
from cadenza.core.interval import Interval
from cadenza.core.inversion import Inversion
from cadenza.core.library import Library
from cadenza.core.note import Note
from cadenza.core.note_letter import NoteLetter
from cadenza.core.organ_args import OrganArgs
from cadenza.core.organ_pipe_family import OrganPipeFamily
from cadenza.core.organ_pipe_length import OrganPipeLength
from cadenza.core.pitch import Pitch
from cadenza.core.quality import Quality
from cadenza.core.scale_degree import ScaleDegree
from cadenza.core.scale_type import ScaleType
from cadenza.core.song import Song
from cadenza.core.transposer import Transposer
from cadenza.core.tremolo_args import TremoloArgs
from cadenza.core.voicing import Voicing

__version__ = importlib.metadata.version("cadenza-music")

__all__ = [
    "Accidental",
    "Alteration",
    "Chord",
    "Composer",
    "DiatonicKey",
    "DiatonicMode",
    "DiatonicScale",
    "Duration",
    "Envelope",
    "Extension",
    "FunctionalAnalysis",
    "Interval",
    "Inversion",
    "Library",
    "Note",
    "NoteLetter",
    "OrganArgs",
    "OrganPipeFamily",
    "OrganPipeLength",
    "ParseError",
    "Pitch",
    "Quality",
    "ScaleDegree",
    "ScaleType",
    "Song",
    "Transposer",
    "TremoloArgs",
    "Voicing",
    "__version__",
]
