from pathlib import Path

from cadenza import DiatonicScale, Library, Note, Transposer


class TestE2EModulate:
    def test_modulate_washed_by_the_water_up_three_semitones(self) -> None:
        library_filepath = Path(__file__).parent.parent / "src" / "cadenza" / "data" / "songs.yaml"
        library = Library.from_file(library_filepath)

        song = next(library.search("Washed by the Water"))
        assert song.title == "Washed by the Water"
        assert song.key is not None
        assert song.key.root == Note.new_b()

        # Modulate up a minor third (3 semitones), from B major to D major
        scale = DiatonicScale.major(Note.new_d())
        modulated_song = Transposer.transpose_song(song, 3, scale=scale)
        assert modulated_song.key is not None
        assert modulated_song.key.root == Note.new_d()

        chords_str = "\n".join(" ".join(str(chord) for chord in line) for line in modulated_song.chords)
        assert chords_str == (
            "D G2 Bm A\n"
            "D D/F♯ G Bm G D G\n"
            "D D/F♯ G Bm G D G\n"
            "D D/F♯ G Bm G D G\n"
            "D D/F♯ G G/A\n"
            "D D/F♯ G G/A\n"
            "D D/F♯ G G/A\n"
            "D D/F♯ G G/A\n"
            "Bm G D\n"
            "Bm G D\n"
            "Bm G D\n"
            "A G\n"
            "D D/F♯ G G/A\n"
            "D D/F♯ G G/A\n"
            "D D/F♯ G G/A\n"
            "D D/F♯ G G/A\n"
            "D D/F♯ G G/A\n"
            "D D/F♯ G G/A\n"
            "D D/F♯ G G/A\n"
            "D D/F♯ G G/A\n"
            "D G Bm A\n"
            "D G Bm A\n"
            "D G Bm A\n"
            "D"
        )
