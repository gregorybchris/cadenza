# Cadenza

## About

Exploration of music theory

## Installation

Install using [uv](https://docs.astral.sh/uv)

```bash
uv sync
```

## Usage examples

### Chord command

Play a single chord

```bash
# Play a chord
cz chord A

# Play a different voicing/inversion
cz chord Bbm7 --inversion 2

# Change the octave (default is 4)
cz chord G#m7 --octave 3

# Transpose a chord up or down by a number of semitones
cz chord G#m7 --transpose 2

# Change the duration of the notes (default is 3 seconds)
cz chord Em --duration 1

# Add pipe organ overtones
cz chord F#dim --overtones

# Add tremolo
cz chord E7b9/G# --tremolo

# Analyze a chord without playing it
cz chord Dmaj7 --no-play

# Save chord audio to a file
cz chord F/G --filepath audio.wav

# Save chord audio to a file with a different sample rate
cz chord Cmaj7/A --filepath audio.wav --sample-rate 48000
```

### Chords command

Play a series of chords

```bash
# Play several chords in a loop
cz chords --tempo 60 --repeat 3 "E C#madd9 Amaj7"
```

### Song command

Play a full song

```bash
# Play a song by title
cz song homesick

# Change the octave (default is 4)
cz song homesick --octave 5

# Transpose a song into a different key by a number of semitones
cz song homesick --transpose -2

# Change the tempo (in beats per minute)
cz song homesick --tempo 120

# Change the duration of each chord
cz song homesick --chord-duration eighth

# Change the note associated with one beat
cz song homesick --beat-duration half

# Add pipe organ overtones
cz song homesick --overtones

# Add tremolo
cz song homesick --tremolo

# Save song audio to a file
cz song homesick --filepath audio.wav

# Save a song to a file without playing it
cz song homesick --filepath audio.wav --no-play

# Save song audio to a file with a different sample rate
cz song homesick --filepath audio.wav --sample-rate 48000
```
