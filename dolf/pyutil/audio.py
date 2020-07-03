import mutagen
from mutagen.mp3 import MP3


def which_encoding(file_path: str) -> str:
    try:
        # Most of the voice-over wav files are actually mp3 files with .wav extensions
        info = MP3(file_path).info
        encoding = "mp3"
    except mutagen.mp3.HeaderNotFoundError:
        # Probably a real wav file
        encoding = "wav"

    return encoding
