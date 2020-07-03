#!/usr/bin/env python3
import re
import captions
import os
from parse import parse_valve_txt

# The folder containing 'portal2.exe'
game_dir = r'C:/Program Files (x86)/Steam/steamapps/common/Portal 2'

# The levels of the game to search through. Not sure what to call this.
# DLC means downloadable content, but it looks like these simply contain the data for official updates.
dlc_dirs = [
    'portal2',
    'portal2_dlc1',
    'portal2_dlc2',
]

output_dir = '../../scripts'


def file_contains(file_path: str, needle: str) -> bool:
    """
    True if the text file contains the given string.
    """
    with open(file_path, 'r') as f:
        return needle.lower() in f.read().lower()


def find_scripts(bad_keys, dlc_dir):
    """
    Find all script files that we need to override, along with the keys that need to muted in each script.
    """
    scripts = []
    for root, dirs, files in os.walk(os.path.join(game_dir, dlc_dir, 'scripts')):
        for name in files:
            if not name.endswith('.txt'):
                continue

            script_path = os.path.join(root, name)
            script_bad_keys = [key for key in bad_keys if file_contains(script_path, key)]
            if len(script_bad_keys):
                scripts.append({
                    'path': script_path,
                    'keys': script_bad_keys,
                })
    return scripts


def case_insensitive_replace(haystack: str, needle: str, replacement: str) -> str:
    """
    Perform case-insensitive string replacement by compiling a regex.
    """
    regex = re.compile(re.escape(needle), re.IGNORECASE)
    return regex.sub(replacement, haystack)


def grab_and_modify_scripts_from_dlc_dir(dlc_dir):
    bad_keys = list(captions.get_bad_keys(os.path.join(game_dir, dlc_dir, 'resource', 'subtitles_english.txt')))
    scripts = find_scripts(bad_keys, dlc_dir)
    for script in scripts:
        grab_script_while_muting_some_parts(dlc_dir, script['path'], script['keys'])


def grab_script_while_muting_some_parts(dlc_dir, script_path, keys):
    """
    Copy the given script file to our mod while muting the given keys by changing the wave property to "silence.wav"
    """
    scripts_encoding = 'UTF-8'

    with open(script_path, 'r', encoding=scripts_encoding) as f:
        raw_data = f.read()

    parsed = parse_valve_txt(raw_data)

    for key in keys:
        entry = parsed[key]
        raw_data = raw_data.replace(entry['wave'], 'silence.wav')

    rel_path = os.path.relpath(script_path, os.path.join(game_dir, dlc_dir, 'scripts'))
    out_path = os.path.join(output_dir, rel_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    with open(out_path, 'w', encoding=scripts_encoding) as f:
        f.write(raw_data)


def main():
    for dlc_dir in dlc_dirs:
        grab_and_modify_scripts_from_dlc_dir(dlc_dir)


if __name__ == '__main__':
    main()
