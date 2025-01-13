import logging
from pathlib import Path
from typing import TYPE_CHECKING

from rich.logging import RichHandler
from typer import Typer

from cadenza import Chord
from cadenza.duration import Duration
from cadenza.note import Note
from cadenza.player import Player
from cadenza.saver import Saver
from cadenza.song_library import SongLibrary
from cadenza.synth import Synth, SynthArgs

if TYPE_CHECKING:
    from torch import Tensor

logger = logging.getLogger(__name__)


app = Typer(pretty_exceptions_enable=False)


def set_logger_config(info: bool, debug: bool) -> None:
    handlers = [RichHandler(rich_tracebacks=True)]
    log_format = "%(message)s"

    if info:
        logging.basicConfig(level=logging.INFO, handlers=handlers, format=log_format)
    if debug:
        logging.basicConfig(level=logging.DEBUG, handlers=handlers, format=log_format)


@app.command()
def go(
    info: bool = False,
    debug: bool = False,
) -> None:
    set_logger_config(info, debug)

    sample_rate = 44_100

    synth_args = SynthArgs(sample_rate=sample_rate)
    synth = Synth(args=synth_args)

    reference_note = Note.from_str("A")
    reference_frequency = 440.0  # A4

    tempo = 120
    beat_value = Duration.Quarter
    chord_duration = Duration.Quarter
    beats_per_chord = chord_duration.get_n_quarter_notes() / beat_value.get_n_quarter_notes()
    beats_per_second = tempo / 60
    seconds_per_chord = beats_per_chord / beats_per_second

    song = SongLibrary.DANCING_THROUGH_LIFE
    segments: list[Tensor] = []
    for chord in song.iter_chords():
        segment = synth.generate_chord_audio(
            chord,
            reference_note,
            reference_frequency,
            seconds_per_chord,
        )
        segments.append(segment)

        audio_silence = synth.generate_silence(0.05)
        segments.append(audio_silence)

    audio = synth.concat(segments)

    player = Player(sample_rate=sample_rate)
    player.play(audio)

    saver = Saver(sample_rate=sample_rate)
    audio_filepath = Path("data/output.wav")
    saver.save(audio, audio_filepath)


@app.command()
def parse(
    chord_str: str,
    info: bool = False,
    debug: bool = False,
) -> None:
    set_logger_config(info, debug)
    chord = Chord.from_str(chord_str)
    print(chord.__repr__())
    print(chord.__str__())
