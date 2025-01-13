def add_symbols(s: str) -> str:
    return s.replace("#", "♯").replace("b", "♭").replace("halfdim", "ø").replace("aug", "+")


def remove_symbols(s: str) -> str:
    return s.replace("♯", "#").replace("♭", "b").replace("ø", "halfdim").replace("+", "aug")


def process_symbols(s: str, symbols: bool) -> str:
    return add_symbols(s) if symbols else remove_symbols(s)
