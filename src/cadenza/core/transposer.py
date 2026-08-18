import logging
from copy import deepcopy
from dataclasses import dataclass
from typing import Optional

from cadenza.core.chord import Chord
from cadenza.core.constants import N_NOTES
from cadenza.core.diatonic_key import DiatonicKey
from cadenza.core.note import Note
from cadenza.core.pitch import Pitch
from cadenza.core.song import Song
from cadenza.core.speller import Speller

logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class Transposer:
    """Move notes and chords by an interval, spelling the result by the function it serves.

    Every method here comes in a safe form that is given a tonic and an unsafe form that is not.
    A pitch class on its own has no spelling: what makes 8 a G♯ rather than an A♭ is the function
    it serves in a key. The unsafe forms have no key to appeal to, so they fall back to keeping the
    letter the note arrived with, moved by the interval. That is a reasonable guess and nothing
    more — an unsafe transposition can return a spelling that makes no sense in the music it lands
    in, and callers that know the key should always pass it.
    """

    @classmethod
    def transpose_note(cls, note: Note, semitones: int, *, tonic: Note) -> Note:
        """Transpose a note, spelling the result by its function in the key of the given tonic."""
        return Speller.spell_from_tonic((note.to_integer() + semitones) % N_NOTES, tonic)

    @classmethod
    def transpose_note_unsafe(cls, note: Note, semitones: int) -> Note:
        """Transpose a note with no key to spell it against. See the note on this class."""
        return Speller.spell_from_root((note.to_integer() + semitones) % N_NOTES, note)

    @classmethod
    def transpose_pitch_unsafe(cls, pitch: Pitch, semitones: int) -> Pitch:
        """Transpose a pitch with no key to spell it against. See the note on this class.

        There is no safe counterpart: pitches are transposed to build the notes of a chord out of
        its intervals, where the anchor is the chord root rather than any tonic.
        """
        new_index = pitch.note.to_integer() + semitones
        note = Speller.spell_from_root(new_index % N_NOTES, pitch.note)
        return Pitch(note=note, octave=pitch.octave + new_index // N_NOTES)

    @classmethod
    def _transpose_chord(cls, chord: Chord, semitones: int, tonic: Optional[Note]) -> Chord:
        root_pitch_class = (chord.root.to_integer() + semitones) % N_NOTES
        if tonic is None:
            root = Speller.spell_from_root(root_pitch_class, chord.root)
        else:
            root = Speller.spell_from_tonic(root_pitch_class, tonic, chord.quality)

        bass = None
        if chord.bass:
            bass_pitch_class = (chord.bass.to_integer() + semitones) % N_NOTES
            if tonic is None or chord.contains_pitch_class(chord.bass.to_integer()):
                bass = Speller.spell_from_root(bass_pitch_class, root)
            else:
                bass = Speller.spell_from_tonic(bass_pitch_class, tonic)

        return chord.model_copy(update={"root": root, "bass": bass})

    @classmethod
    def transpose_chord(cls, chord: Chord, semitones: int, *, tonic: Note) -> Chord:
        """Transpose a chord, spelling each note by the function it serves.

        The root is spelled by its function in the key, so a chord built a tritone above the tonic
        of C is F♯ (the leading tone into V) rather than G♭. The bass is spelled by its function in
        the chord whenever it is a chord tone, so the bass of E7/G♯ stays G♯ — the third of E7 —
        even though that pitch class is the flattened sixth of C. A bass that is not a chord tone
        has no function in the chord to take a spelling from, so it falls back to the key.
        """
        return cls._transpose_chord(chord, semitones, tonic)

    @classmethod
    def transpose_chord_unsafe(cls, chord: Chord, semitones: int) -> Chord:
        """Transpose a chord with no key to spell it against. See the note on this class."""
        return cls._transpose_chord(chord, semitones, None)

    @classmethod
    def _transpose_song(cls, song: Song, semitones: int, tonic: Optional[Note]) -> Song:
        new_song = deepcopy(song)
        if tonic is not None and song.key is not None:
            new_song.key = DiatonicKey(root=tonic, mode=song.key.mode)
        new_song.chords = [[cls._transpose_chord(c, semitones, tonic) for c in line] for line in song.chords]
        if new_song.voicings is not None:
            for voicing in new_song.voicings:
                voicing.chord = cls._transpose_chord(voicing.chord, semitones, tonic)
        return new_song

    @classmethod
    def transpose_song(cls, song: Song, semitones: int) -> Song:
        """Transpose a keyed song, spelling its chords by their function in the destination key.

        The destination key follows from the key the song started in and the interval it moved by,
        so a song in F♯ stays in F♯ when it is not transposed at all, and every chord spelling
        follows from there.

        Raises a ValueError for a song with no key, which has no function for its chords to serve.
        Use transpose_song_unsafe for those, knowing what it costs.
        """
        if song.key is None:
            msg = f"The song '{song.title}' has no key to spell its chords against. Use transpose_song_unsafe."
            raise ValueError(msg)

        pitch_class = (song.key.root.to_integer() + semitones) % N_NOTES
        return cls._transpose_song(song, semitones, Speller.spell_key(pitch_class, song.key.root))

    @classmethod
    def transpose_song_unsafe(cls, song: Song, semitones: int) -> Song:
        """Transpose a song with no key to spell it against. See the note on this class."""
        return cls._transpose_song(song, semitones, None)
