import logging
from copy import deepcopy
from dataclasses import dataclass

from cadenza.chord import Chord
from cadenza.constants import N_NOTES
from cadenza.diatonic_key import DiatonicKey
from cadenza.diatonic_scale import DiatonicScale
from cadenza.note import Note
from cadenza.pitch import Pitch
from cadenza.song import Song

logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class Transposer:
    @classmethod
    def transpose_note(cls, note: Note, semitones: int, *, scale: DiatonicScale) -> Note:
        new_index = (note.to_integer() + semitones) % N_NOTES
        # NOTE: This unsafe call is ok because we find the correct enharmonic note directly after
        new_note = Note.from_integer_unsafe(new_index)
        for scale_note in scale.get_notes():
            if new_note.is_enharmonic(scale_note):
                return scale_note
        return new_note

    @classmethod
    def transpose_pitch(cls, pitch: Pitch, semitones: int, *, scale: DiatonicScale) -> Pitch:
        new_note = cls.transpose_note(pitch.note, semitones, scale=scale)
        new_octave = pitch.octave + (pitch.note.to_integer() + semitones) // N_NOTES
        return Pitch(note=new_note, octave=new_octave)

    @classmethod
    def transpose_chord(cls, chord: Chord, semitones: int, *, scale: DiatonicScale) -> Chord:
        new_chord = deepcopy(chord)
        new_chord.root = cls.transpose_note(chord.root, semitones, scale=scale)
        new_chord.bass = cls.transpose_note(chord.bass, semitones, scale=scale) if chord.bass else None
        return new_chord

    @classmethod
    def transpose_song(cls, song: Song, semitones: int, *, scale: DiatonicScale) -> Song:
        new_song = deepcopy(song)
        new_song.chords = [[cls.transpose_chord(c, semitones, scale=scale) for c in line] for line in song.chords]
        if new_song.key is not None:
            new_root = cls.transpose_note(new_song.key.root, semitones, scale=scale)
            new_song.key = DiatonicKey(root=new_root, mode=new_song.key.mode)
        new_voicings = None
        if new_song.voicings is not None:
            new_voicings = []
            for voicing in new_song.voicings:
                new_voicing = deepcopy(voicing)
                new_voicing.chord = cls.transpose_chord(voicing.chord, semitones, scale=scale)
                new_voicings.append(new_voicing)
        new_song.voicings = new_voicings
        return new_song

    @classmethod
    def transpose_note_unsafe(cls, note: Note, semitones: int) -> "Note":
        new_index = (note.to_integer() + semitones) % N_NOTES
        return Note.from_integer_unsafe(new_index)

    @classmethod
    def transpose_pitch_unsafe(cls, pitch: Pitch, semitones: int) -> Pitch:
        new_note = cls.transpose_note_unsafe(pitch.note, semitones)
        new_octave = pitch.octave + (pitch.note.to_integer() + semitones) // N_NOTES
        return Pitch(note=new_note, octave=new_octave)

    @classmethod
    def transpose_chord_unsafe(cls, chord: Chord, semitones: int) -> "Chord":
        new_root = cls.transpose_note_unsafe(chord.root, semitones)
        new_bass = cls.transpose_note_unsafe(chord.bass, semitones) if chord.bass else None
        return Chord(
            root=new_root,
            quality=chord.quality,
            extension=chord.extension,
            alteration=chord.alteration,
            bass=new_bass,
        )

    @classmethod
    def transpose_song_unsafe(cls, song: Song, semitones: int) -> Song:
        new_song = deepcopy(song)
        new_song.chords = [[cls.transpose_chord_unsafe(c, semitones) for c in line] for line in song.chords]
        if new_song.key is not None:
            new_root = cls.transpose_note_unsafe(new_song.key.root, semitones)
            new_song.key = DiatonicKey(root=new_root, mode=new_song.key.mode)
        new_voicings = None
        if new_song.voicings is not None:
            new_voicings = []
            for voicing in new_song.voicings:
                new_voicing = deepcopy(voicing)
                new_voicing.chord = cls.transpose_chord_unsafe(voicing.chord, semitones)
                new_voicings.append(new_voicing)
        new_song.voicings = new_voicings
        return new_song
