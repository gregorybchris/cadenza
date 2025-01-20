from cadenza.duration import Duration
from cadenza.song import Song


class SongLibrary:
    @classmethod
    def get(cls, slug: str) -> Song:  # noqa: PLR0911
        if slug == "range-rover":
            return cls.RANGE_ROVER
        if slug == "dancing-through-life":
            return cls.DANCING_THROUGH_LIFE
        if slug == "dancing-my-way":
            return cls.DANCING_MY_WAY
        if slug == "homesick":
            return cls.HOMESICK
        if slug == "put-your-records-on":
            return cls.PUT_YOUR_RECORDS_ON
        if slug == "only-home-ive-ever-known":
            return cls.ONLY_HOME_IVE_EVER_KNOWN
        if slug == "dont-stop-believin":
            return cls.DONT_STOP_BELIEVIN
        if slug == "talk-is-cheap":
            return cls.TALK_IS_CHEAP

        msg = f"Unknown song slug: {slug}"
        raise ValueError(msg)

    RANGE_ROVER = Song.from_str(
        "Range Rover",
        "Ben Rector",
        """
D F#m Bm G
D F#m Bm D7 G D E7 G
D F# Bm D7 G D E7 G/A
D D D""",
        tempo=35,
        beat_duration=Duration.Whole,
        chord_duration=Duration.Whole,
    )

    DANCING_THROUGH_LIFE = Song.from_str(
        "Dancing Through Life",
        "Wicked",
        """
G Cm/G G Adim G
D Em C Am D
G D#aug
Em G C9 C Ahalfdim D#
G G#dim7 Am7
E Emaj7 E Emaj7
E Emaj7 A B B C#m7
Am
C D
E Emaj7 A
""",
        tempo=80,
        beat_duration=Duration.Eighth,
        chord_duration=Duration.Quarter,
    )

    DANCING_MY_WAY = Song.from_str(
        "Dancing My Way",
        "Wyn Starks",
        """
C G Am F C G Am F
Dm Am G Dm Am G
F Am F Am F Am F Am
C Dm Am F C Dm Am F
Dm Am G Dm Am G
F Am F Am F Am F Am
Fm C Bb F Fm C Bb F Fm C Bb F
F Am F Am F Am F Am F Am F Am F Am F Am
""",
        tempo=80,
        beat_duration=Duration.Eighth,
        chord_duration=Duration.Half,
    )

    HOMESICK = Song.from_str(
        "Homesick",
        "Noah Kahan",
        """
F# D#m C# B
F# D#m C# B
""",
    )

    PUT_YOUR_RECORDS_ON = Song.from_str(
        "Put Your Records On",
        "Corinne Bailey Rae",
        """
Bb C7 Eb/F Bb
Gm7 D7/F# Gm7 C
""",
    )

    ONLY_HOME_IVE_EVER_KNOWN = Song.from_str(
        "Only Home I've Ever Known",
        "The California Honeydrops",
        """
Eb Ab Eb G Cm Faug Bb7 Eb
Eb Ab Ab Ab Eb
Bb G7/B Cm F7 Bb7
Bb G7 Cm Ab G7
Ab F7/A Eb/Bb G7/B Cm
F7 Bb7 Eb
Bb Eb Bb Eb G7 Cm
F7 Bb7
Bb Ab Eb
""",
    )

    DONT_STOP_BELIEVIN = Song.from_str(
        "Don't Stop Believin'",
        "Journey",
        """
E B C#m A
""",
    )

    TALK_IS_CHEAP = Song.from_str(
        "Talk is Cheap",
        "Kyle Thornton",
        """
Bbm7 Bbm7/Eb Abmaj7 F7/A
Ab F7 F7/A Bbm7
""",
    )
