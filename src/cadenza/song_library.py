from cadenza.song import Song


class SongLibrary:
    RANGE_ROVER = Song.from_str(
        "Range Rover",
        "Ben Rector",
        """
D F#m Bm G
D F#m Bm D7 G D E7 G
D F# Bm D7 G D E7 G
D D D""",
    )

    DANCING_THROUGH_LIFE = Song.from_str(
        "Dancing Through Life",
        "Wicked",
        """
G Cm G Adim G
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
    )

    HOME_SICK = Song.from_str(
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
Bb C7 Ebsus2 Bb
Gm7 D7 Gm7 C
""",
    )

    ONLY_HOME_IVE_EVER_KNOWN = Song.from_str(
        "Only Home I've Ever Known",
        "The California Honeydrops",
        """
Eb Ab Eb G Cm Faug Bb7 Eb
Eb Ab Ab Ab Eb
Bb G7 Cm F7 Bb7
Bb G7 Cm Ab G7
Ab F7 Eb G7 Cm
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
