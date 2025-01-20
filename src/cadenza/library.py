import re
from pathlib import Path
from typing import Iterator, Self

import yaml
from pydantic import BaseModel

from cadenza.song import Song


class Library(BaseModel):
    songs: list[Song]

    @classmethod
    def from_file(cls, filepath: Path) -> Self:
        with filepath.open("r") as file:
            data = yaml.safe_load(file)
        return cls(**data)

    def search(self, query: str) -> Iterator[Song]:
        for song in self.songs:
            if (
                re.search(query, song.title, re.IGNORECASE)
                or re.search(query, song.artist, re.IGNORECASE)
                or query == song.id
            ):
                yield song
