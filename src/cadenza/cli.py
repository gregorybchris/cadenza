import logging
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Optional

from rich.console import Console
from rich.logging import RichHandler
from typer import Argument, Option, Typer

from cadenza import Chord
from cadenza.duration import Duration
from cadenza.inversion import Inversion
from cadenza.player import Player
from cadenza.saver import Saver
from cadenza.song_library import SongLibrary
from cadenza.synth import Synth, SynthArgs
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
def chord(  # noqa: PLR0913
    chord_str: Annotated[str, Argument(...)],
    octave: Annotated[int, Option("--octave")] = 4,
    inversion_num: Annotated[int, Option("--inversion")] = 0,
    duration_s: Annotated[float, Option("--duration", "-d")] = 3.0,
    overtones: Annotated[bool, Option("--overtones/--no-overtones")] = False,
    sample_rate: Annotated[int, Option("--sample-rate", "-sr")] = 44_100,
    play: Annotated[bool, Option("--play/--no-play")] = True,
    show_pitches: Annotated[bool, Option("--show-pitches/--no-show-pitches")] = True,
    filepath: Optional[Path] = None,
    info: bool = False,
    debug: bool = False,
) -> None:
    set_logger_config(info, debug)
    inversion = Inversion.from_number(inversion_num)
    chord = Chord.from_str(chord_str)
    console.print(chord)
    console.print(f"[red]{chord}")

    synth_args = SynthArgs(sample_rate=sample_rate)
    synth = Synth(args=synth_args)

    voicing = Voicing(chord=chord, inversion=inversion, octave=octave)
    audio = synth.generate_voicing_audio(voicing, duration_s, overtones=overtones)

    if show_pitches:
        pitches = voicing.get_pitches()
        for pitch in pitches:
            console.print(f"[bold][white]{pitch.note}{pitch.octave}[bright_black]: [red]{pitch.get_frequency():.1f} Hz")

    if play:
        player = Player(sample_rate=sample_rate)
        player.play(audio)

    if filepath:
        saver = Saver(sample_rate=sample_rate)
        saver.save(audio, filepath)


@app.command()
def song(  # noqa: PLR0913
    slug: str,
    octave: Annotated[int, Option("--octave")] = 4,
    tempo: Annotated[Optional[float], Option("--tempo")] = None,
    chord_duration: Optional[Duration] = None,
    beat_duration: Optional[Duration] = None,
    overtones: Annotated[bool, Option("--overtones/--no-overtones")] = False,
    sample_rate: int = 44_100,
    play: Annotated[bool, Option("--play/--no-play")] = True,
    filepath: Optional[Path] = None,
    info: bool = False,
    debug: bool = False,
) -> None:
    set_logger_config(info, debug)

    synth_args = SynthArgs(sample_rate=sample_rate)
    synth = Synth(args=synth_args)

    # Select a song from the library to generate
    song = SongLibrary.get(slug)

    tempo = tempo or song.tempo
    beat_duration = beat_duration or song.beat_duration
    chord_duration = chord_duration or song.chord_duration

    beats_per_chord = chord_duration.get_n_quarter_notes() / beat_duration.get_n_quarter_notes()
    beats_per_second = tempo / 60
    seconds_per_chord = beats_per_chord / beats_per_second
    silence_duration = seconds_per_chord / 20
    audio_duration = seconds_per_chord - silence_duration

    segments: list[Tensor] = []
    for chord in song.iter_chords():
        voicing = Voicing(chord=chord, inversion=Inversion.Root, octave=octave)
        segment = synth.generate_voicing_audio(voicing, audio_duration, overtones=overtones)
        segments.append(segment)

        audio_silence = synth.generate_silence(silence_duration)
        segments.append(audio_silence)

    audio = synth.concat(segments)

    if play:
        player = Player(sample_rate=sample_rate)
        player.play(audio)

    if filepath:
        saver = Saver(sample_rate=sample_rate)
        saver.save(audio, filepath)
