import logging

from cadenza.chord import Chord
from cadenza.constants import N_NOTES
from cadenza.diatonic_scale import DiatonicScale
from cadenza.extension import Extension
from cadenza.interval import Interval
from cadenza.note import Note
from cadenza.quality import Quality
from cadenza.scale_degree import ScaleDegree
from cadenza.transposer import Transposer

logger = logging.getLogger(__name__)


class FunctionalAnalysis:
    @classmethod
    def get_chord_function_str(cls, chord: Chord, root: Note) -> str:  # noqa: PLR0912
        interval_int = (chord.root.to_integer() - root.to_integer()) % N_NOTES
        interval = Interval.from_int(interval_int)
        try:
            scale_degree = ScaleDegree.from_interval(interval)
        except ValueError as exc:
            msg = f"Failed to convert chord {chord} to a scale degree: {exc}"
            logger.debug(msg)
            return "?"

        function = scale_degree.to_symbol()

        # TODO: use match case to avoid dropping cases
        if chord.quality in [Quality.Minor, Quality.Diminished, Quality.HalfDiminished]:
            function = function.lower()
        if chord.quality == Quality.Diminished:
            function += Quality.Diminished.to_str()
        if chord.quality == Quality.Augmented:
            function += Quality.Augmented.to_str()
        if chord.quality == Quality.HalfDiminished:
            function += Quality.HalfDiminished.to_str()
        if chord.extension == Extension.Seven:
            function += Extension.Seven.to_str()
        if chord.extension == Extension.MajorSeven:
            function += Extension.MajorSeven.to_str()
        if chord.extension == Extension.Nine:
            function += Extension.Nine.to_str()
        if chord.extension == Extension.MajorNine:
            function += Extension.MajorNine.to_str()
        if chord.extension == Extension.Eleven:
            function += Extension.Eleven.to_str()
        if chord.extension == Extension.Thirteen:
            function += Extension.Thirteen.to_str()
        if chord.quality == Quality.SusTwo:
            function += Quality.SusTwo.to_str()
        if chord.quality == Quality.SusFour:
            function += Quality.SusFour.to_str()

        if chord.bass is not None:
            base_interval_int = (chord.bass.to_integer() - root.to_integer()) % N_NOTES
            base_interval = Interval.from_int(base_interval_int)
            try:
                base_scale_degree = ScaleDegree.from_interval(base_interval)
            except ValueError as exc:
                msg = f"Failed to convert chord {chord} bass to a scale degree: {exc}"
                logger.debug(msg)
                return str(chord)
            base_function = base_scale_degree.to_symbol()
            function += f"/{base_function}"

        return function

    @classmethod
    def function_to_chord(cls, tonic: Chord, scale_degree: ScaleDegree) -> Chord:
        transpose = Transposer.transpose_note
        root = tonic.root
        match tonic.quality:
            case Quality.Major:
                scale = DiatonicScale.major(root)
                return {
                    ScaleDegree.Tonic: Chord(root=transpose(root, 0, scale=scale), quality=Quality.Major),
                    ScaleDegree.Supertonic: Chord(root=transpose(root, 2, scale=scale), quality=Quality.Minor),
                    ScaleDegree.Mediant: Chord(root=transpose(root, 4, scale=scale), quality=Quality.Minor),
                    ScaleDegree.Subdominant: Chord(root=transpose(root, 5, scale=scale), quality=Quality.Major),
                    ScaleDegree.Dominant: Chord(root=transpose(root, 7, scale=scale), quality=Quality.Major),
                    ScaleDegree.Submediant: Chord(root=transpose(root, 9, scale=scale), quality=Quality.Minor),
                    ScaleDegree.LeadingTone: Chord(root=transpose(root, 11, scale=scale), quality=Quality.Diminished),
                }[scale_degree]
            case Quality.Minor:
                scale = DiatonicScale.minor(root)
                return {
                    ScaleDegree.Tonic: Chord(root=transpose(root, 0, scale=scale), quality=Quality.Minor),
                    ScaleDegree.Supertonic: Chord(root=transpose(root, 2, scale=scale), quality=Quality.Diminished),
                    ScaleDegree.Mediant: Chord(root=transpose(root, 3, scale=scale), quality=Quality.Major),
                    ScaleDegree.Subdominant: Chord(root=transpose(root, 5, scale=scale), quality=Quality.Minor),
                    ScaleDegree.Dominant: Chord(root=transpose(root, 7, scale=scale), quality=Quality.Minor),
                    ScaleDegree.Submediant: Chord(root=transpose(root, 8, scale=scale), quality=Quality.Major),
                    ScaleDegree.LeadingTone: Chord(root=transpose(root, 10, scale=scale), quality=Quality.Minor),
                }[scale_degree]
            case _:
                msg = f"Getting chords by degree for quality {tonic.quality.to_written()} is not supported"
                raise ValueError(msg)
