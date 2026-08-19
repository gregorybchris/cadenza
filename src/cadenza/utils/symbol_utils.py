from cadenza.core.constants import (
    AUG_CHARS,
    AUG_SYMBOL,
    DIM_CHARS,
    DIM_SYMBOL,
    DOUBLE_FLAT_CHARS,
    DOUBLE_FLAT_SYMBOL,
    DOUBLE_SHARP_CHARS,
    DOUBLE_SHARP_SYMBOL,
    FLAT_CHAR,
    FLAT_SYMBOL,
    HALFDIM_CHARS,
    HALFDIM_SYMBOL,
    MIN_CHARS,
    MIN_SYMBOL,
    SHARP_CHAR,
    SHARP_SYMBOL,
)


def add_symbols(s: str) -> str:
    # NOTE: Replace double accidentals before single ones to avoid partial matches
    # NOTE: Replace halfdim before dim to avoid partial matches
    # NOTE: Replace halfdim and dim before min to avoid partial matches
    return (
        s.replace(DOUBLE_SHARP_CHARS, DOUBLE_SHARP_SYMBOL)
        .replace(DOUBLE_FLAT_CHARS, DOUBLE_FLAT_SYMBOL)
        .replace(SHARP_CHAR, SHARP_SYMBOL)
        .replace(FLAT_CHAR, FLAT_SYMBOL)
        .replace(HALFDIM_CHARS, HALFDIM_SYMBOL)
        .replace(DIM_CHARS, DIM_SYMBOL)
        .replace(AUG_CHARS, AUG_SYMBOL)
        .replace(MIN_CHARS, MIN_SYMBOL)
    )


def remove_symbols(s: str) -> str:
    return (
        s.replace(DOUBLE_SHARP_SYMBOL, DOUBLE_SHARP_CHARS)
        .replace(DOUBLE_FLAT_SYMBOL, DOUBLE_FLAT_CHARS)
        .replace(SHARP_SYMBOL, SHARP_CHAR)
        .replace(FLAT_SYMBOL, FLAT_CHAR)
        .replace(HALFDIM_SYMBOL, HALFDIM_CHARS)
        .replace(DIM_SYMBOL, DIM_CHARS)
        .replace(AUG_SYMBOL, AUG_CHARS)
        .replace(MIN_SYMBOL, MIN_CHARS)
    )
