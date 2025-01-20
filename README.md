# Cadenza

## About

Exploration of music theory

## Installation

Install using [uv](https://docs.astral.sh/uv)

```bash
uv sync
```

## Usage examples

### Chords

```bash
# Play a chord
cz chord A

# Play a different voicing/inversion
cz chord Bbm7 --inversion 2

# Change the octave (default is 4)
cz chord G#m7 --octave 3

# Change the duration of the notes (default is 3 seconds)
cz chord Em --duration 1

# Add overtones
cz chord F#dim --overtones

# Analyze a chord without playing it
cz chord Dmaj7 --no-play

# Save chord audio to a file
cz chord F/G --filepath audio.wav

# Save chord audio to a file with a different sample rate
cz chord Cmaj7/A --filepath audio.wav --sample-rate 48000
```

### Songs

```bash
# Play a song by title
cz song homesick

# Change the octave (default is 4)
cz song homesick --octave 5

# Change the tempo (in beats per minute)
cz song homesick --tempo 120

# Change the duration of each chord
cz song homesick --chord-duration eighth

# Change the note associated with one beat
cz song homesick --beat-duration half

# Add overtones
cz song homesick --overtones

# Save song audio to a file
cz song homesick --filepath audio.wav

# Save a song to a file without playing it
cz song homesick --filepath audio.wav --no-play

# Save song audio to a file with a different sample rate
cz song homesick --filepath audio.wav --sample-rate 48000
```
