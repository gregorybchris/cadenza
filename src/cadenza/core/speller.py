import logging
from dataclasses import dataclass
from typing import ClassVar, Optional

from cadenza.core.constants import N_NOTES
from cadenza.core.note import Note
from cadenza.core.note_letter import NoteLetter
from cadenza.core.quality import Quality

logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class Speller:
    """Choose enharmonic spellings from a note's function rather than from its pitch class alone.

    A pitch class on its own has no spelling: 8 is both G♯ and A♭. What decides is the interval
    from some anchor, because an interval carries a generic size (how many letters to move) as
    well as a number of semitones. Moving 8 semitones and 5 letters up from C gives A♭, while
    moving 8 semitones and 4 letters up from C gives G♯.

    Chord roots are anchored to the tonic, so they spell by their function in the key. Chord tones
    are anchored to the chord root, so they spell by their function in the chord: the third of E7
    is G♯ regardless of what the key would call that pitch class.
    """

    # NOTE: Generic size of each interval in semitones, measured up from a tonic. The chromatic
    # degrees take their usual spellings in tonal music: ♭2 (Neapolitan), ♭3, ♯4 (the secondary
    # leading tone into V), ♭6 and ♭7 (borrowed from the parallel minor). These hold for both
    # major and minor tonics, which differ in which degrees are diatonic but not in their letters.
    GENERIC_SIZES_FROM_TONIC: ClassVar[dict[int, int]] = {
        0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 5, 9: 5, 10: 6, 11: 6,
    }  # fmt: skip

    # NOTE: A diminished chord on the flattened sixth is nearly always the leading tone chord into
    # vi rather than a chord on ♭6, so it takes the raised fifth: D♯° in G major, not E♭°. The other
    # chromatic degrees keep their usual spellings, which is what the songs in the library use.
    GENERIC_SIZES_FROM_TONIC_DIMINISHED: ClassVar[dict[int, int]] = {**GENERIC_SIZES_FROM_TONIC, 8: 4}

    # NOTE: Measured up from a chord root, a tritone is the lowered fifth of the chord rather
    # than a raised fourth, so it takes one more letter than it would from a tonic.
    GENERIC_SIZES_FROM_ROOT: ClassVar[dict[int, int]] = {**GENERIC_SIZES_FROM_TONIC, 6: 4}

    @classmethod
    def _spell(cls, pitch_class: int, anchor: Note, generic_sizes: dict[int, int]) -> Note:
        semitones = (pitch_class - anchor.to_integer()) % N_NOTES
        letter = NoteLetter.from_index(anchor.letter.to_index() + generic_sizes[semitones])

        # The letter fixes the spelling, so the accidentals are whatever closes the remaining gap
        return Note.from_letter_and_pitch_class(letter, pitch_class)

    @classmethod
    def spell_from_tonic(cls, pitch_class: int, tonic: Note, quality: Optional[Quality] = None) -> Note:
        """Spell a pitch class by its function in the key of the given tonic."""
        if quality == Quality.Diminished:
            note = cls._spell(pitch_class, tonic, cls.GENERIC_SIZES_FROM_TONIC_DIMINISHED)
            # NOTE: The raised spelling is only worth having while it stays readable. The leading
            # tone chord into vi is D♯° in G major, but spelling it that way in F♯ major would take
            # a double sharp, and there D° reads better than C𝄪°.
            if note.n_sharps + note.n_flats <= 1:
                return note
        return cls._spell(pitch_class, tonic, cls.GENERIC_SIZES_FROM_TONIC)

    @classmethod
    def spell_from_root(cls, pitch_class: int, root: Note) -> Note:
        """Spell a pitch class by its interval above the given chord root."""
        return cls._spell(pitch_class, root, cls.GENERIC_SIZES_FROM_ROOT)

    @classmethod
    def spell_key(cls, pitch_class: int, source: Note) -> Note:
        """Spell the key a song lands in when it moves from the given key to the given pitch class.

        The interval from the old key names the new one, so a song in C moved up two semitones is
        in D rather than C𝄪. Where that would take more than one accidental the plainest name for
        the pitch class wins instead, because a key signature has to be readable: a song in A♭
        moved up a semitone is in A, not B♭♭.
        """
        tonic = cls.spell_from_root(pitch_class, source)
        if tonic.n_sharps + tonic.n_flats <= 1:
            return tonic

        # NOTE: The interval only ever overshoots by reaching across a black key from a flat key,
        # which lands on a natural. Anything with no natural to fall back on was reached from a key
        # too remote to spell in the first place, so its derived spelling stands.
        natural = Note.natural_from_integer(pitch_class)
        return natural if natural is not None else tonic
