import logging
from typing import Self

from pydantic import BaseModel

from cadenza.alteration import Alteration
from cadenza.chord import Chord
from cadenza.extension import Extension
from cadenza.interval import Interval
from cadenza.inversion import Inversion
from cadenza.pitch import Pitch
from cadenza.quality import Quality

logger = logging.getLogger(__name__)


class Voicing(BaseModel):
    chord: Chord
    inversion: Inversion
    octave: int

    @classmethod
    def from_chord(cls, chord: Chord, inversion: Inversion, octave: int) -> Self:
        return cls(chord=chord, inversion=inversion, octave=octave)

    def _get_intervals_from_quality(self) -> list[Interval]:  # noqa: PLR0911
        match self.chord.quality:
            case Quality.Major:
                return [Interval.MajorThird, Interval.PerfectFifth]
            case Quality.Minor:
                return [Interval.MinorThird, Interval.PerfectFifth]
            case Quality.Diminished:
                return [Interval.MinorThird, Interval.Tritone]
            case Quality.Augmented:
                return [Interval.MajorThird, Interval.MinorSixth]
            case Quality.HalfDiminished:
                return [Interval.MinorThird, Interval.Tritone, Interval.MinorSeventh]
            case Quality.SusTwo:
                return [Interval.MajorSecond, Interval.PerfectFifth]
            case Quality.SusFour:
                return [Interval.PerfectFourth, Interval.PerfectFifth]

    def _get_intervals_from_extension(self) -> list[Interval]:
        if not self.chord.extension:
            return []
        match self.chord.extension:
            case Extension.Seven:
                return [Interval.MinorSeventh]
            case Extension.MajorSeven:
                return [Interval.MajorSeventh]
            case Extension.AddNine:
                return [Interval.MajorSecond]
            case Extension.AddEleven:
                return [Interval.PerfectFourth]
            case Extension.AddThirteen:
                return [Interval.MajorSixth]

    def _get_intervals_from_alteration(self) -> list[Interval]:
        if not self.chord.alteration:
            return []
        match self.chord.alteration:
            case Alteration.FlatFive:
                return [Interval.Tritone]

    def _get_intervals_from_bass(self) -> list[Interval]:
        if not self.chord.bass:
            return []
        return [Interval.from_int(self.chord.bass.to_index() - self.chord.root.to_index())]

    def get_pitches(self) -> list[Pitch]:
        rh_intervals: list[Interval] = []
        rh_intervals += [Interval.Unison]
        rh_intervals += self._get_intervals_from_quality()
        rh_intervals += self._get_intervals_from_extension()
        rh_intervals += self._get_intervals_from_alteration()

        rh_notes = [self.chord.root + interval.to_int() for interval in rh_intervals]

        inversion_number = self.inversion.get_number()
        n_rh_notes = len(rh_notes)
        if inversion_number >= n_rh_notes:
            msg = f"The {self.inversion.to_written()} does not exist for a voicing with {n_rh_notes} right hand notes."
            logger.error(msg)
            raise ValueError(msg)

        rh_pitches = [Pitch(note=note, octave=self.octave) for note in rh_notes]

        for _ in range(inversion_number):
            transposed_pitch = rh_pitches[0]
            transposed_pitch.octave += 1
            rh_pitches = rh_pitches[1:] + [transposed_pitch]

        lh_intervals: list[Interval] = []
        lh_intervals += self._get_intervals_from_bass()
        if len(lh_intervals) == 0:
            lh_intervals += [Interval.Unison]
        lh_notes = [self.chord.root + interval.to_int() for interval in lh_intervals]
        lh_pitches = [Pitch(note=note, octave=self.octave - 2) for note in lh_notes]

        return lh_pitches + rh_pitches
