import logging
import re
from typing import Iterator, Optional, Self

from pydantic import BaseModel

from cadenza.alteration import Alteration
from cadenza.errors import ParseError
from cadenza.extension import Extension
from cadenza.note import Note
from cadenza.quality import Quality
from cadenza.scale_degree import ScaleDegree

logger = logging.getLogger(__name__)


class Chord(BaseModel):
    root: Note
    quality: Quality
    extension: Optional[Extension] = None
    alteration: Optional[Alteration] = None

    @classmethod
    def from_str(cls, chord_str: str) -> Self:
        regex = (
            r"^([A-Ga-g](♯|#|♭|b)?)"  # Root
            r"(m|min|dim|aug|\+|ø|halfdim|sus2|sus4)?"  # Quality
            r"(add\d+|7|maj7|9|11|13)?"  # Extension
            r"([♯#♭b]\d+)?$"  # Alteration
        )
        match = re.match(regex, chord_str)
        if not match:
            msg = f"Failed to parse chord string: {chord_str}"
            raise ParseError(msg)
        root_str, _, quality_str, extension_str, alteration_str = match.groups()

        root = Note.from_str(root_str)
        quality = Quality.from_str(quality_str) if quality_str else Quality.Major
        extension = Extension.from_str(extension_str) if extension_str else None
        alteration = Alteration.from_str(alteration_str) if alteration_str else None
        return cls(root=root, quality=quality, extension=extension, alteration=alteration)

    def __str__(self) -> str:
        extension_str = "" if self.extension is None else self.extension.to_str()
        alterations_str = "" if self.alteration is None else self.alteration.to_str()
        return f"{self.root}{self.quality}{extension_str}{alterations_str}"

    def iter_notes(self) -> Iterator[Note]:
        raise NotImplementedError

    @classmethod
    def from_scale_degree(cls, tonic: "Chord", scale_degree: ScaleDegree) -> Self:
        root = tonic.root
        match tonic.quality:
            case Quality.Major:
                return {
                    ScaleDegree.Tonic: cls(root=root, quality=Quality.Major),
                    ScaleDegree.Supertonic: cls(root=root + 2, quality=Quality.Minor),
                    ScaleDegree.Mediant: cls(root=root + 4, quality=Quality.Minor),
                    ScaleDegree.Subdominant: cls(root=root + 5, quality=Quality.Major),
                    ScaleDegree.Dominant: cls(root=root + 7, quality=Quality.Major),
                    ScaleDegree.Submediant: cls(root=root + 9, quality=Quality.Minor),
                    ScaleDegree.LeadingTone: cls(root=root + 10, quality=Quality.Diminished),
                }[scale_degree]
            case Quality.Minor:
                return {
                    ScaleDegree.Tonic: cls(root=root, quality=Quality.Minor),
                    ScaleDegree.Supertonic: cls(root=root + 2, quality=Quality.Diminished),
                    ScaleDegree.Mediant: cls(root=root + 3, quality=Quality.Major),
                    ScaleDegree.Subdominant: cls(root=root + 5, quality=Quality.Minor),
                    ScaleDegree.Dominant: cls(root=root + 6, quality=Quality.Minor),
                    ScaleDegree.Submediant: cls(root=root + 8, quality=Quality.Major),
                    ScaleDegree.LeadingTone: cls(root=root + 10, quality=Quality.Minor),
                }[scale_degree]
            case _:
                msg = f"Getting chords by degree for quality {tonic.quality.to_written()} is not supported"
                raise ValueError(msg)
