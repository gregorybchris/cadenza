import logging
import math
from dataclasses import dataclass

from cadenza.alteration import Alteration
from cadenza.constants import N_NOTES
from cadenza.diatonic_scale import DiatonicScale
from cadenza.extension import Extension
from cadenza.interval import Interval
from cadenza.note import Note
from cadenza.pitch import Pitch
from cadenza.quality import Quality
from cadenza.transposer import Transposer
from cadenza.voicing import Voicing

logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class Composer:
    @classmethod
    def frequency_to_pitch(cls, frequency: float) -> Pitch:
        lowest_pitch = Pitch(note=Note.new_c(), octave=1)
        # NOTE: Offset slightly to allow for rounding errors
        lowest_pitch_frequency = cls.pitch_to_frequency(lowest_pitch) - 0.1
        if frequency < lowest_pitch_frequency:
            msg = f"Frequency {frequency} is lower than lowest allowed frequency {lowest_pitch_frequency}"
            raise ValueError(msg)

        n_semitones = round(N_NOTES * (math.log2(frequency) - math.log2(Pitch.REFERENCE_FREQUENCY)))
        n_octaves = n_semitones // N_NOTES
        n_degrees = n_semitones % N_NOTES
        # NOTE: This unsafe call is inevitable because we have no key information from a frequency.
        note = Transposer.transpose_note_unsafe(Pitch.REFERENCE_NOTE, n_degrees)
        octave = Pitch.REFERENCE_OCTAVE + n_octaves
        return Pitch(note=note, octave=octave)

    @classmethod
    def pitch_to_frequency(cls, pitch: Pitch) -> float:
        degree_difference = pitch.note.to_integer() - Pitch.REFERENCE_NOTE.to_integer()
        octave_difference = pitch.octave - Pitch.REFERENCE_OCTAVE
        n_semitones = degree_difference + octave_difference * N_NOTES
        return Pitch.REFERENCE_FREQUENCY * 2 ** (n_semitones / N_NOTES)

    @classmethod
    def _get_intervals_from_quality(cls, voicing: Voicing) -> list[Interval]:  # noqa: PLR0911
        match voicing.chord.quality:
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

    @classmethod
    def _get_intervals_from_extension(cls, voicing: Voicing) -> list[Interval]:  # noqa: PLR0911
        if not voicing.chord.extension:
            return []
        match voicing.chord.extension:
            case Extension.Seven:
                return [Interval.MinorSeventh]
            case Extension.MajorSeven:
                return [Interval.MajorSeventh]
            case Extension.Nine:
                # NOTE: The 9 chord includes all previous extensions (the 7th).
                return [Interval.MinorSeventh, Interval.MajorNinth]
            case Extension.MajorNine:
                # NOTE: The maj9 chord includes all previous extensions (the 7th).
                return [Interval.MajorSeventh, Interval.MajorNinth]
            case Extension.Eleven:
                # NOTE: The 11 chord includes all previous extensions (the 7th and 9th).
                return [Interval.MinorSeventh, Interval.MajorNinth, Interval.PerfectEleventh]
            case Extension.Thirteen:
                # NOTE: Often the 13 chord is played without the 11th,
                # though both are accepted voicings.
                return [Interval.MinorSeventh, Interval.MajorNinth, Interval.MajorThirteenth]

    @classmethod
    def _update_intervals_from_alteration(cls, voicing: Voicing, intervals: list[Interval]) -> None:
        if not voicing.chord.alteration:
            return
        match voicing.chord.alteration:
            case Alteration.AddTwo:
                intervals.append(Interval.MajorSecond)
            case Alteration.AddFour:
                intervals.append(Interval.PerfectFourth)
            case Alteration.AddSix:
                match voicing.chord.quality:
                    case Quality.Major:
                        intervals.append(Interval.MajorSixth)
                    case Quality.Minor:
                        intervals.append(Interval.MinorSixth)
                    case _:
                        msg = f"Invalid quality for add6: {voicing.chord.quality}"
                        raise ValueError(msg)
            case Alteration.AddNine:
                intervals.append(Interval.MajorNinth)
            case Alteration.FlatFive:
                intervals.remove(Interval.PerfectFifth)
                intervals.append(Interval.Tritone)
            case Alteration.FlatNine:
                intervals.append(Interval.MinorNinth)

    @classmethod
    def _get_intervals_from_bass(cls, voicing: Voicing) -> list[Interval]:
        if not voicing.chord.bass:
            return []
        interval_int = (voicing.chord.bass.to_integer() - voicing.chord.root.to_integer()) % N_NOTES
        return [Interval.from_int(interval_int)]

    @classmethod
    def _apply_inversion(cls, voicing: Voicing, pitches: list[Pitch]) -> list[Pitch]:
        inversion_number = voicing.inversion.to_number()
        n_notes = len(pitches)
        if inversion_number >= n_notes:
            msg = f"The {voicing.inversion.to_written()} does not exist for a voicing with {n_notes} right hand notes."
            raise ValueError(msg)

        for _ in range(inversion_number):
            pitches[0].octave += 1
            pitches = pitches[1:] + [pitches[0]]
        return pitches

    @classmethod
    def _get_scale(cls, voicing: Voicing) -> DiatonicScale:
        if voicing.chord.quality in [Quality.Minor, Quality.Diminished, Quality.HalfDiminished]:
            return DiatonicScale.minor(voicing.chord.root)
        return DiatonicScale.major(voicing.chord.root)

    @classmethod
    def voicing_to_pitches(cls, voicing: Voicing) -> list[Pitch]:
        scale = cls._get_scale(voicing)

        lh_pitches: list[Pitch] = []
        if voicing.include_left_hand:
            lh_intervals: list[Interval] = []
            lh_intervals += cls._get_intervals_from_bass(voicing)
            if len(lh_intervals) == 0:
                lh_intervals += [Interval.Unison]
            lh_root_pitch = Pitch(note=voicing.chord.root, octave=voicing.octave - 2)
            lh_pitches = [Transposer.transpose_pitch(lh_root_pitch, x.to_int(), scale=scale) for x in lh_intervals]

        rh_intervals: list[Interval] = []
        rh_intervals += [Interval.Unison]
        rh_intervals += cls._get_intervals_from_quality(voicing)
        rh_intervals += cls._get_intervals_from_extension(voicing)
        cls._update_intervals_from_alteration(voicing, rh_intervals)
        rh_root_pitch = Pitch(note=voicing.chord.root, octave=voicing.octave)
        rh_pitches = [Transposer.transpose_pitch(rh_root_pitch, x.to_int(), scale=scale) for x in rh_intervals]
        rh_pitches = cls._apply_inversion(voicing, rh_pitches)

        return lh_pitches + rh_pitches
