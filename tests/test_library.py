from pathlib import Path

from cadenza.core.library import Library


class TestLibrary:
    def test_from_file(self) -> None:
        library_filepath = Path(__file__).parent / "data" / "library.yaml"
        Library.from_file(library_filepath)
