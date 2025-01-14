import logging
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Optional

from rich.console import Console
from rich.logging import RichHandler
from typer import Option, Typer

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
    chord_str: str,
    octave: int = 4,
    sample_rate: int = 44_100,
    duration_s: float = 3.0,
    overtones: Annotated[bool, Option("--overtones/--no-overtones")] = False,
    play: Annotated[bool, Option("--play/--no-play")] = True,
    show_pitches: Annotated[bool, Option("--show-pitches/--no-show-pitches")] = True,
    filepath: Optional[Path] = None,
    info: bool = False,
    debug: bool = False,
) -> None:
    set_logger_config(info, debug)
    chord = Chord.from_str(chord_str)
    console.print(chord)
    console.print(f"[red]{chord}")

    synth_args = SynthArgs(sample_rate=sample_rate)
    synth = Synth(args=synth_args)

    voicing = Voicing(chord=chord, inversion=Inversion.Root, octave=octave)
    audio = synth.generate_voicing_audio(voicing, duration_s, overtones=overtones)

    if show_pitches:
        pitches = voicing.get_pitches()
        for pitch in pitches:
            console.print(
                f"[bold][white]{pitch.note} "
                f"[bright_black]([blue]{pitch.octave}[bright_black]): "
                f"[red]{pitch.get_frequency():.1f} Hz"
            )

    if play:
        player = Player(sample_rate=sample_rate)
        player.play(audio)

    if filepath:
        saver = Saver(sample_rate=sample_rate)
        saver.save(audio, filepath)


@app.command()
def song(  # noqa: PLR0913
    slug: str,
    octave: int = 4,
    tempo: Optional[int] = None,
    beat_value: Optional[Duration] = None,
    chord_duration: Optional[Duration] = None,
    sample_rate: int = 44_100,
    overtones: Annotated[bool, Option("--overtones/--no-overtones")] = False,
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
    beat_value = beat_value or song.beat_value
    chord_duration = chord_duration or song.chord_duration

    beats_per_chord = chord_duration.get_n_quarter_notes() / beat_value.get_n_quarter_notes()
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
