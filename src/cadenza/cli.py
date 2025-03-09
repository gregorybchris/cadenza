import logging
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Optional

import torch
from rich.console import Console
from rich.logging import RichHandler
from typer import Argument, Option, Typer

from cadenza.chord import Chord
from cadenza.composer import Composer
from cadenza.diatonic_scale import DiatonicScale
from cadenza.duration import Duration
from cadenza.functional_analysis import FunctionalAnalysis
from cadenza.inversion import Inversion
from cadenza.library import Library
from cadenza.note import Note
from cadenza.optimizer import Optimizer, OptimizerArgs
from cadenza.pitch import Pitch
from cadenza.player import Player
from cadenza.saver import Saver
from cadenza.synth import Synth, SynthArgs
from cadenza.transposer import Transposer
from cadenza.voicing import Voicing

if TYPE_CHECKING:
    from torch import Tensor

logger = logging.getLogger(__name__)


app = Typer(pretty_exceptions_enable=False)
console = Console()


def set_logger_config(info: bool, debug: bool) -> None:
    handlers = [RichHandler(rich_tracebacks=True)]
    log_format = "%(message)s"

    if info:
        logging.basicConfig(level=logging.INFO, handlers=handlers, format=log_format)
    if debug:
        logging.basicConfig(level=logging.DEBUG, handlers=handlers, format=log_format)


@app.command()
def note(  # noqa: PLR0913
    note_str: Annotated[str, Argument(...)],
    octave: Annotated[int, Option("--octave")] = 4,
    transpose: Annotated[int, Option("--transpose")] = 0,
    duration_s: Annotated[float, Option("--duration", "-d")] = 3.0,
    overtones: Annotated[bool, Option("--overtones/--no-overtones")] = False,
    tremolo: Annotated[bool, Option("--tremolo/--no-tremolo")] = False,
    sample_rate: int = 44_100,
    show_symbols: Annotated[bool, Option("--symbols/--no-symbols")] = True,
    play: Annotated[bool, Option("--play/--no-play")] = True,
    show_pitch: Annotated[bool, Option("--pitch/--no-pitch")] = True,
    filepath: Optional[Path] = None,
    info: bool = False,
    debug: bool = False,
) -> None:
    set_logger_config(info, debug)

    note = Note.from_str(note_str)
    note = Transposer.transpose_note(note, transpose, scale=DiatonicScale.major(note))
    pitch = Pitch(note=note, octave=octave)

    synth_args = SynthArgs(sample_rate=sample_rate)
    synth = Synth(args=synth_args)

    frequencies = torch.tensor([Composer.pitch_to_frequency(pitch)])
    audio = synth.generate(frequencies, duration_s, overtones=overtones)

    if tremolo:
        audio = synth.apply_hammond_tremolo(audio)

    if show_pitch:
        frequency = Composer.pitch_to_frequency(pitch)
        console.print(
            f"[bold][white]{pitch.note.to_str(symbols=show_symbols)}"
            f"[blue]{pitch.octave}[bright_black]: [green]{frequency:.1f} Hz"
        )

    if filepath:
        saver = Saver(sample_rate=sample_rate)
        saver.save(audio, filepath)

    if play:
        player = Player(sample_rate=sample_rate)
        player.play(audio)


@app.command()
def chord(  # noqa: PLR0913
    chord_str: Annotated[str, Argument(...)],
    octave: Annotated[int, Option("--octave")] = 4,
    inversion_num: Annotated[int, Option("--inversion")] = 0,
    transpose: Annotated[int, Option("--transpose")] = 0,
    duration_s: Annotated[float, Option("--duration", "-d")] = 3.0,
    overtones: Annotated[bool, Option("--overtones/--no-overtones")] = False,
    tremolo: Annotated[bool, Option("--tremolo/--no-tremolo")] = False,
    sample_rate: Annotated[int, Option("--sample-rate", "-sr")] = 44_100,
    show_symbols: Annotated[bool, Option("--symbols/--no-symbols")] = True,
    include_left_hand: Annotated[bool, Option("--include-left-hand/--no-left-hand")] = False,
    play: Annotated[bool, Option("--play/--no-play")] = True,
    show_pitches: Annotated[bool, Option("--pitches/--no-pitches")] = True,
    filepath: Optional[Path] = None,
    info: bool = False,
    debug: bool = False,
) -> None:
    set_logger_config(info, debug)

    inversion = Inversion.from_number(inversion_num)
    chord = Chord.from_str(chord_str)
    chord = Transposer.transpose_chord_unsafe(chord, transpose)
    console.print(f"[red]{chord.to_str(symbols=show_symbols)}")

    synth_args = SynthArgs(sample_rate=sample_rate)
    synth = Synth(args=synth_args)

    voicing = Voicing(chord=chord, inversion=inversion, octave=octave, include_left_hand=include_left_hand)
    pitches = Composer.voicing_to_pitches(voicing)
    frequencies = torch.tensor([Composer.pitch_to_frequency(pitch) for pitch in pitches])
    audio = synth.generate(frequencies, duration_s, overtones=overtones)

    if tremolo:
        audio = synth.apply_hammond_tremolo(audio)

    if show_pitches:
        for pitch in pitches:
            frequency = Composer.pitch_to_frequency(pitch)
            console.print(
                f"[bold][white]{pitch.note.to_str(symbols=show_symbols)}"
                f"[blue]{pitch.octave}[bright_black]: [green]{frequency:.1f} Hz"
            )

    if filepath:
        saver = Saver(sample_rate=sample_rate)
        saver.save(audio, filepath)

    if play:
        player = Player(sample_rate=sample_rate)
        player.play(audio)


@app.command()
def chords(  # noqa: PLR0913
    chords_str: str,
    octave: Annotated[int, Option("--octave")] = 4,
    inversion_num: Annotated[int, Option("--inversion")] = 0,
    transpose: Annotated[int, Option("--transpose")] = 0,
    tempo: Annotated[float, Option("--tempo")] = 80.0,
    chord_duration: Duration = Duration.Quarter,
    beat_duration: Duration = Duration.Quarter,
    repeat: Annotated[int, Option("--repeat")] = 1,
    overtones: Annotated[bool, Option("--overtones/--no-overtones")] = False,
    tremolo: Annotated[bool, Option("--tremolo/--no-tremolo")] = False,
    sample_rate: int = 44_100,
    include_left_hand: Annotated[bool, Option("--include-left-hand/--no-left-hand")] = False,
    play: Annotated[bool, Option("--play/--no-play")] = True,
    filepath: Optional[Path] = None,
    info: bool = False,
    debug: bool = False,
) -> None:
    set_logger_config(info, debug)

    synth_args = SynthArgs(sample_rate=sample_rate)
    synth = Synth(args=synth_args)

    beats_per_chord = chord_duration.get_n_quarter_notes() / beat_duration.get_n_quarter_notes()
    beats_per_second = tempo / 60
    seconds_per_chord = beats_per_chord / beats_per_second
    silence_duration = seconds_per_chord / 20
    audio_duration = seconds_per_chord - silence_duration

    segments: list[Tensor] = []
    chords = [Chord.from_str(chord_str) for chord_str in chords_str.split()]
    chords = [Transposer.transpose_chord_unsafe(chord, transpose) for chord in chords]
    inversion = Inversion.from_number(inversion_num)
    for _ in range(repeat):
        for chord in chords:
            voicing = Voicing.from_chord(chord, inversion, octave, include_left_hand=include_left_hand)
            pitches = Composer.voicing_to_pitches(voicing)
            frequencies = torch.tensor([Composer.pitch_to_frequency(pitch) for pitch in pitches])
            segment = synth.generate(frequencies, audio_duration, overtones=overtones)
            segments.append(segment)

            audio_silence = synth.generate_silence(silence_duration)
            segments.append(audio_silence)

    audio = synth.concat(segments)

    if tremolo:
        audio = synth.apply_hammond_tremolo(audio)

    if filepath:
        saver = Saver(sample_rate=sample_rate)
        saver.save(audio, filepath)

    if play:
        player = Player(sample_rate=sample_rate)
        player.play(audio)


@app.command()
def song(  # noqa: PLR0912, PLR0913, PLR0915
    query: str,
    octave: Annotated[int, Option("--octave")] = 4,
    transpose: Annotated[int, Option("--transpose")] = 0,
    tempo: Annotated[Optional[float], Option("--tempo")] = None,
    chord_duration: Optional[Duration] = None,
    beat_duration: Optional[Duration] = None,
    repeat: Annotated[int, Option("--repeat")] = 1,
    overtones: Annotated[bool, Option("--overtones/--no-overtones")] = False,
    tremolo: Annotated[bool, Option("--tremolo/--no-tremolo")] = False,
    sample_rate: int = 44_100,
    show_symbols: Annotated[bool, Option("--symbols/--no-symbols")] = True,
    show_functions: Annotated[bool, Option("--functions/--no-functions")] = False,
    play: Annotated[bool, Option("--play/--no-play")] = True,
    start_line: Annotated[int, Option("--line")] = 1,
    spacious: Annotated[bool, Option("--spacious/--no-spacious")] = False,
    filepath: Optional[Path] = None,
    info: bool = False,
    debug: bool = False,
) -> None:
    set_logger_config(info, debug)

    synth_args = SynthArgs(sample_rate=sample_rate)
    synth = Synth(args=synth_args)

    library_filepath = Path(__file__).parent / "data" / "songs.yaml"
    library = Library.from_file(library_filepath)
    results_iter = library.search(query)

    try:
        song = next(results_iter)
    except StopIteration:
        msg = f"No song found for query: {query}"
        console.print(f"[bold][red]{msg}")
        return

    if song.key is None:
        song = Transposer.transpose_song_unsafe(song, transpose)
    else:
        scale = DiatonicScale.major(song.key.root)
        song = Transposer.transpose_song(song, transpose, scale=scale)

    # Apply overrides
    tempo = tempo or song.tempo
    beat_duration = beat_duration or song.beat_duration
    chord_duration = chord_duration or song.chord_duration

    console.print(f"Title: [bold][white]{song.title}")
    console.print(f"Artist: [bold][white]{song.artist}")
    console.print(f"Tempo: [bold][white]{tempo:.0f}bpm")
    console.print(f"Beat duration: [bold][white]{beat_duration}")
    console.print(f"Chord duration: [bold][white]{chord_duration}")
    if song.key is not None:
        console.print(f"Key: [bold][white]{song.key.root.to_str(symbols=show_symbols)} {song.key.mode.to_str()}")
    if transpose != 0:
        console.print(f"Transpose: [bold][white]{transpose}")
    console.print("Chords:")
    for chord_line in song.chords:
        if show_functions:
            if song.key is None:
                msg = "Cannot display functional analysis with an unknown key"
                console.print(f"[bold][red]{msg}")
                return

            functions = [FunctionalAnalysis.get_chord_function_str(chord, song.key.root) for chord in chord_line]
            function_line_str = "[white]   [bold][green]".join(str(function) for function in functions)
            console.print(f"[bold][green]{function_line_str}")

        chord_line_str = "[white] | [bold][blue]".join(chord.to_str(symbols=show_symbols) for chord in chord_line)
        console.print(f"[bold][blue]{chord_line_str}")

        if spacious:
            console.print()

    beats_per_chord = chord_duration.get_n_quarter_notes() / beat_duration.get_n_quarter_notes()
    beats_per_second = tempo / 60
    seconds_per_chord = beats_per_chord / beats_per_second
    silence_duration = 0  # Can be seconds_per_chord / 20 for some space
    audio_duration = seconds_per_chord - silence_duration

    if start_line - 1 >= len(song.chords):
        msg = f"Start line is greater than the number of lines in the song: {len(song.chords)}"
        console.print(f"[bold][red]{msg}")
        return

    segments: list[Tensor] = []
    for _ in range(repeat):
        for chord_line_num, chord_line in enumerate(song.chords):
            if chord_line_num < start_line - 1:
                continue
            for chord in chord_line:
                voicing = Voicing.from_chord(chord, Inversion.Root, octave)
                if song.voicings is not None:
                    for voicing_override in song.voicings:
                        if voicing_override.chord == chord:
                            voicing = Voicing(
                                chord=voicing_override.chord,
                                inversion=voicing_override.inversion,
                                octave=voicing_override.octave,
                            )
                            break

                pitches = Composer.voicing_to_pitches(voicing)
                frequencies = torch.tensor([Composer.pitch_to_frequency(pitch) for pitch in pitches])
                segment = synth.generate(frequencies, audio_duration, overtones=overtones)
                segments.append(segment)

                audio_silence = synth.generate_silence(silence_duration)
                segments.append(audio_silence)

    audio = synth.concat(segments)

    if tremolo:
        audio = synth.apply_hammond_tremolo(audio)

    if filepath:
        saver = Saver(sample_rate=sample_rate)
        saver.save(audio, filepath)

    if play:
        player = Player(sample_rate=sample_rate)
        player.play(audio)


@app.command()
def optimize(  # noqa: PLR0913
    chord_str: Annotated[str, Argument(...)],
    octave: Annotated[int, Option("--octave")] = 4,
    inversion_num: Annotated[int, Option("--inversion")] = 0,
    transpose: Annotated[int, Option("--transpose")] = 0,
    duration_s: Annotated[float, Option("--duration", "-d")] = 3.0,
    sample_rate: Annotated[int, Option("--sample-rate", "-sr")] = 44_100,
    show_symbols: Annotated[bool, Option("--symbols/--no-symbols")] = True,
    include_left_hand: Annotated[bool, Option("--include-left-hand/--no-left-hand")] = False,
    play: Annotated[bool, Option("--play/--no-play")] = True,
    show_pitches: Annotated[bool, Option("--pitches/--no-pitches")] = True,
    unoptimized_filepath: Optional[Path] = None,
    optimized_filepath: Optional[Path] = None,
    n_epochs: Annotated[int, Option("--n-epochs")] = 1000,
    learning_rate: Annotated[float, Option("--learning-rate", "-lr")] = 0.01,
    max_denominator: Annotated[int, Option("--max-denominator")] = 6,
    convergence_threshold: Annotated[int, Option("--convergence-threshold")] = 10,
    status_interval: Annotated[int, Option("--status-interval")] = 100,
    info: bool = False,
    debug: bool = False,
) -> None:
    set_logger_config(info, debug)

    inversion = Inversion.from_number(inversion_num)
    chord = Chord.from_str(chord_str)
    chord = Transposer.transpose_chord_unsafe(chord, transpose)
    console.print(chord)
    console.print(f"[red]{chord.to_str(symbols=show_symbols)}")

    voicing = Voicing(chord=chord, inversion=inversion, octave=octave, include_left_hand=include_left_hand)
    pitches = Composer.voicing_to_pitches(voicing)
    unoptimized_frequencies = torch.tensor([Composer.pitch_to_frequency(pitch) for pitch in pitches])

    optimizer_args = OptimizerArgs(
        n_epochs=n_epochs,
        learning_rate=learning_rate,
        max_denominator=max_denominator,
        convergence_threshold=convergence_threshold,
        status_interval=status_interval,
    )
    optimizer = Optimizer(args=optimizer_args)
    optimized_frequencies = optimizer.optimize(unoptimized_frequencies)

    synth_args = SynthArgs(sample_rate=sample_rate)
    synth = Synth(args=synth_args)
    unoptimized_audio = synth.generate(unoptimized_frequencies, duration_s, overtones=False)
    optimized_audio = synth.generate(optimized_frequencies, duration_s, overtones=False)

    if show_pitches:
        for pitch in pitches:
            frequency = Composer.pitch_to_frequency(pitch)
            console.print(
                f"[bold][white]{pitch.note.to_str(symbols=show_symbols)}"
                f"[blue]{pitch.octave}[bright_black]: [green]{frequency:.1f} Hz"
            )

    console.print("\nInitial Chord:", unoptimized_frequencies.numpy().round(1))
    optimizer.print_frequency_ratios(console, unoptimized_frequencies)
    console.print("\nFinal Chord:", optimized_frequencies.numpy().round(1))
    optimizer.print_frequency_ratios(console, optimized_frequencies)

    if unoptimized_filepath:
        saver = Saver(sample_rate=sample_rate)
        saver.save(unoptimized_audio, unoptimized_filepath)

    if optimized_filepath:
        saver = Saver(sample_rate=sample_rate)
        saver.save(optimized_audio, optimized_filepath)

    if play:
        player = Player(sample_rate=sample_rate)
        player.play(unoptimized_audio)
        player.play(optimized_audio)
