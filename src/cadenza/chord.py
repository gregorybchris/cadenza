import logging
import re
from typing import Iterator, Optional, Self

from pydantic import BaseModel

from cadenza.alteration import Alteration
from cadenza.extension import Extension
from cadenza.note import Note
from cadenza.quality import Quality

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
            msg = f"Invalid chord string: {chord_str}"
            raise ValueError(msg)
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
    def get_chord(cls, root: "Chord", degree: int) -> Self:  # noqa: PLR0911, PLR0912
        mod = degree % 8
        match root.quality:
            case Quality.Major:
                if mod == 1:
                    return cls(root=root.root, quality=Quality.Major)
                if mod == 2:  # noqa: PLR2004
                    return cls(root=root.root + 2, quality=Quality.Minor)
                if mod == 3:  # noqa: PLR2004
                    return cls(root=root.root + 3, quality=Quality.Minor)
                if mod == 4:  # noqa: PLR2004
                    return cls(root=root.root + 5, quality=Quality.Major)
                if mod == 5:  # noqa: PLR2004
                    return cls(root=root.root + 7, quality=Quality.Major)
                if mod == 6:  # noqa: PLR2004
                    return cls(root=root.root + 9, quality=Quality.Minor)
                if mod == 7:  # noqa: PLR2004
                    return cls(root=root.root + 10, quality=Quality.Diminished)
            case Quality.Minor:
                if mod == 1:
                    return cls(root=root.root, quality=Quality.Minor)
                if mod == 2:  # noqa: PLR2004
                    return cls(root=root.root + 2, quality=Quality.Diminished)
                if mod == 3:  # noqa: PLR2004
                    return cls(root=root.root + 3, quality=Quality.Major)
                if mod == 4:  # noqa: PLR2004
                    return cls(root=root.root + 5, quality=Quality.Minor)
                if mod == 5:  # noqa: PLR2004
                    return cls(root=root.root + 7, quality=Quality.Minor)
                if mod == 6:  # noqa: PLR2004
                    return cls(root=root.root + 8, quality=Quality.Major)
                if mod == 7:  # noqa: PLR2004
                    return cls(root=root.root + 10, quality=Quality.Minor)
            case _:
                msg = f"Cannot get chord for quality: {root.quality.to_written()}"
                raise ValueError(msg)
        msg = f"Invalid degree: {degree}"
        raise ValueError(msg)
