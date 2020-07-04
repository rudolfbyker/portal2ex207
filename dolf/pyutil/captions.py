from typing import Generator
from parse import load_valve_txt_file


def get_bad_keys(file_name: str) -> Generator[str, None, None]:
    """
    Use plain text captions to find audio files that need to be censored.
    """
    captions = load_valve_txt_file(file_name, 'UTF-16')
    tokens = captions['lang']['tokens']
    return (key for (key, value) in tokens.items() if should_censor(value))


def should_censor(message: str) -> bool:
    """
    Should the given string be censored? Aim for NO false negatives. False positives are not a problem.
    """
    censor = [
        'god',
        'jesus',
        'christ',
        'lord',
        'oh for...',
    ]

    ignore = [
        'richard lord',
        'christen coomer',
        'the gods',
        'the sea god',
        'god of war',
        'thunder god thor',
        'christmas',
    ]

    lower = message.lower()
    for word in ignore:
        lower = lower.replace(word, '')

    for word in censor:
        if word in lower:
            return True

    return False
