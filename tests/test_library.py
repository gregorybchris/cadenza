from pathlib import Path

from cadenza.library import Library


class TestLibrary:
    def test_from_file(self) -> None:
        library_filepath = Path(__file__).parent.parent / "src" / "cadenza" / "data" / "songs.yaml"
        Library.from_file(library_filepath)
