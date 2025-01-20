from typing import ClassVar, Iterator

from pydantic import BaseModel

from cadenza.chord import Chord
from cadenza.duration import Duration


class Song(BaseModel):
    DEFAULT_TEMPO: ClassVar[float] = 80.0
    DEFAULT_BEAT_DURATION: ClassVar[Duration] = Duration.Quarter
    DEFAULT_CHORD_DURATION: ClassVar[Duration] = Duration.Quarter

    name: str
    artist: str
    chords: list[Chord]
    tempo: float = DEFAULT_TEMPO
    beat_duration: Duration = DEFAULT_BEAT_DURATION
    chord_duration: Duration = DEFAULT_CHORD_DURATION

    @classmethod
    def from_str(  # noqa: PLR0913
        cls,
        name: str,
        artist: str,
        song_str: str,
        *,
        tempo: float = DEFAULT_TEMPO,
        beat_duration: Duration = DEFAULT_BEAT_DURATION,
        chord_duration: Duration = DEFAULT_CHORD_DURATION,
    ) -> "Song":
        chord_strs = song_str.replace("\n", " ").strip().split(" ")
        chords = [Chord.from_str(chord_str) for chord_str in chord_strs]
        return cls(
            name=name,
            artist=artist,
            chords=chords,
            tempo=tempo,
            beat_duration=beat_duration,
            chord_duration=chord_duration,
        )

    def iter_chords(self) -> Iterator[Chord]:
        return iter(self.chords)
