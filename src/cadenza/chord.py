import logging
import re
from typing import Optional, Self

from pydantic import BaseModel

from cadenza.alteration import Alteration
from cadenza.errors import ParseError
from cadenza.extension import Extension
from cadenza.note import Note
from cadenza.quality import Quality

logger = logging.getLogger(__name__)


class Chord(BaseModel):
    root: Note
    quality: Quality
    extension: Optional[Extension] = None
    alteration: Optional[Alteration] = None
    bass: Optional[Note] = None

    @classmethod
    def from_str(cls, chord_str: str) -> Self:
        regex = (
            r"^([A-Ga-g](♯|#|♭|b)?)"  # Root
            r"(m|dim|\°|aug|\+|\ø|halfdim)?"  # Quality pre
            r"(7|maj7|9|maj9|11|13)?"  # Extension
            r"((♯|#|♭|b|sharp|flat|add)?\d+)?"  # Alteration
            r"(sus2|sus4)?"  # Quality post
            r"(/([A-Ga-g](♯|#|♭|b)?))?$"  # Optional bass note
        )

        match = re.match(regex, chord_str)
        if not match:
            msg = f"Failed to parse chord string: {chord_str}"
            raise ParseError(msg)
        root_str, _, quality_pre_str, extension_str, alteration_str, _, quality_post_str, _, bass_str, _ = (
            match.groups()
        )

        root = Note.from_str(root_str)
        if quality_pre_str:
            quality = Quality.from_str(quality_pre_str)
        elif quality_post_str:
            quality = Quality.from_str(quality_post_str)
        else:
            quality = Quality.Major
        extension = Extension.from_str(extension_str) if extension_str else None
        alteration = Alteration.from_str(alteration_str) if alteration_str else None
        bass = Note.from_str(bass_str) if bass_str else None
        return cls(root=root, quality=quality, extension=extension, alteration=alteration, bass=bass)

    def to_str(self, symbols: bool = True) -> str:
        extension_str = self.extension.to_str() if self.extension else ""
        alterations_str = self.alteration.to_str(symbols=symbols) if self.alteration else ""
        bass_str = f"/{self.bass.to_str(symbols=symbols)}" if self.bass else ""
        ret = self.root.to_str(symbols=symbols)
        if self.quality.is_prefix():
            ret += self.quality.to_str(symbols=symbols)
        ret += extension_str
        ret += alterations_str
        if self.quality.is_suffix():
            ret += self.quality.to_str(symbols=symbols)
        ret += bass_str
        return ret

    def __str__(self) -> str:
        return self.to_str()
