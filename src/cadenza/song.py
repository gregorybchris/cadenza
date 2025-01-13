from typing import Iterator

from pydantic import BaseModel

from cadenza.chord import Chord


class Song(BaseModel):
    name: str
    artist: str
    chords: list[Chord]

    @classmethod
    def from_str(cls, name: str, artist: str, song_str: str) -> "Song":
        chord_strs = song_str.replace("\n", " ").strip().split(" ")
        chords = [Chord.from_str(chord_str) for chord_str in chord_strs]
        return cls(name=name, artist=artist, chords=chords)

    def iter_chords(self) -> Iterator[Chord]:
        return iter(self.chords)
