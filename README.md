# Cadenza

## Experiments

This repository contains various loosely related experiments related to music theory and audio engineering. Below are some brief descriptions of the experiments.

### Chord parser

The chord parser evaluates a string representation of a chord. It parses out the chord quality, extensions, and alterations. This works for simple chords like C or more complex chords like F#maj7b5/D.

### Overtone/tremolo synthesizer

The synthesizer decomposes a voicing of a chord into frequencies and synthesizes them into an audio waveform. This component also augments the pure tones in the chord with harmonics of the fundamental. The synthesized audio has the timbre of a pipe organ.

The synthesizer also supports tremolo of various speeds. There is a preset for a Hammond organ sound that combines high frequency tremolo with a low frequency Leslie tremolo effect.

### Just intonation optimizer

By default the synthesizer uses a reference frequency of 440.0 Hz (for the pitch A4) to compute other pitches. All pitches are tuned with equal temperament. If you want to convert a chord into just intonation you can run the optimizer to approximate simple ratios for all intervals in the chord.

[A video of oscilloscope visualizations of just intonation vs equal temperament](https://www.youtube.com/watch?v=6NlI4No3s0M)

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

# Apply a lowpass filter
cz chord Cadd6 --overtones --lowpass 120

# Analyze a chord without playing it
cz chord Dmaj7 --no-play

# Save chord audio to a file
cz chord F/G --filepath audio.wav

# Save chord audio to a file with a different sample rate
cz chord Cmaj7/A --filepath audio.wav --sample-rate 48000

# Visualize the mel spectrogram
cz chord A7b5sus2 --visualize
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

# Add reverb
cz song homesick --reverb

# Apply a highpass filter
cz song homesick --overtones --highpass 450

# Save song audio to a file
cz song homesick --filepath audio.wav

# Save a song to a file without playing it
cz song homesick --filepath audio.wav --no-play

# Save song audio to a file with a different sample rate
cz song homesick --filepath audio.wav --sample-rate 48000

# Visualize the mel spectrogram
cz song homesick --visualize
```

### Optimize command

Optimize a chord from equal temperament to just intonation

```bash
# Optimize a chord
cz optimize C

# Turn on debug logging to see the optimization trace
cz optimize C --debug

# Adjust the learning rate to speed up convergence
cz optimize C --debug -lr 0.05

# Optimizing chords with complex frequency ratios requires adjusting the granularity of optimization
cz optimize Cmaj7 --debug --max-denominator 12
```
