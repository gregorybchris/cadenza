from typing import Any, ClassVar, Iterator

from pydantic import BaseModel, model_validator

from cadenza.chord import Chord
from cadenza.duration import Duration

JsonDict = dict[str, Any]


class Song(BaseModel):
    DEFAULT_TEMPO: ClassVar[float] = 80.0
    DEFAULT_BEAT_DURATION: ClassVar[Duration] = Duration.Quarter
    DEFAULT_CHORD_DURATION: ClassVar[Duration] = Duration.Quarter

    id: str
    title: str
    artist: str
    chords: list[list[Chord]]
    tempo: float = DEFAULT_TEMPO
    beat_duration: Duration = DEFAULT_BEAT_DURATION
    chord_duration: Duration = DEFAULT_CHORD_DURATION

    @staticmethod
    def _parse_chords_str(chords_str: str) -> list[list[Chord]]:
        lines = chords_str.splitlines()
        chord_str_lines = [line.split() for line in lines]
        return [[Chord.from_str(chord_str) for chord_str in chord_strs] for chord_strs in chord_str_lines]

    @model_validator(mode="before")
    def transform_fields(cls, values: JsonDict) -> JsonDict:  # noqa: N805
        values["chords"] = cls._parse_chords_str(values["chords"])
        return values

    def iter_chords(self) -> Iterator[Chord]:
        for chord_list in self.chords:
            for chord in chord_list:
                yield chord
