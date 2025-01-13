import logging

from rich.logging import RichHandler
from typer import Typer

from cadenza import Chord

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
