import re
from typing import Any, ClassVar, Iterator, Optional

from pydantic import BaseModel, model_validator

from cadenza.chord import Chord
from cadenza.diatonic_key import DiatonicKey
from cadenza.diatonic_mode import DiatonicMode
from cadenza.duration import Duration
from cadenza.note import Note
from cadenza.voicing import Voicing

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
    key: Optional[DiatonicKey] = None
    voicings: Optional[list[Voicing]] = None

    @staticmethod
    def _parse_chord_line(str_line: str) -> list[list[Chord]]:
        if str_line.startswith("~"):
            return []

        # Regex pulls off a suffix of (x2) from the end of the chord line, e.g. "C G Am F (x2)" and returns the number 2
        chord_lines = []
        repeat_pattern = r"^(.*)\s+\(x(\d+)\)$"
        repeat_match = re.match(repeat_pattern, str_line)
        if repeat_match:
            str_line = repeat_match.group(1)
            repeat_count = int(repeat_match.group(2))
        else:
            repeat_count = 1

        for _ in range(repeat_count):
            chord_line = [Chord.from_str(chord_str) for chord_str in str_line.split()]
            chord_lines.append(chord_line)
        return chord_lines

    @staticmethod
    def _parse_chords_str(chords_str: str) -> list[list[Chord]]:
        str_lines = chords_str.splitlines()
        chord_lines = []
        for str_line in str_lines:
            chord_lines.extend(Song._parse_chord_line(str_line))
        return chord_lines

    @model_validator(mode="before")
    def transform_fields(cls, values: JsonDict) -> JsonDict:  # noqa: N805
        values["chords"] = cls._parse_chords_str(values["chords"])
        if values.get("key"):
            root = Note.from_str(values["key"]["root"])
            mode = DiatonicMode.from_str(values["key"]["mode"])
            values["key"] = DiatonicKey(root=root, mode=mode)
        if values.get("voicings"):
            for voicing_dict in values["voicings"]:
                voicing_dict["chord"] = Chord.from_str(voicing_dict["chord"])
        return values

    def iter_chords(self) -> Iterator[Chord]:
        for chord_list in self.chords:
            for chord in chord_list:
                yield chord
