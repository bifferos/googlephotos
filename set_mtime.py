#!/usr/bin/env python3

import os
import sys
import re
from pathlib import Path
from datetime import datetime



# The forms that are important
DATE_REGEX = [
  re.compile(r"^[^_]+_(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})_(?P<hour>\d{2})(?P<minute>\d{2})(?P<second>\d{2})([-_].+)?$"),
  re.compile(r"^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})[ _](?P<hour>\d{2})\.(?P<minute>\d{2})\.(?P<second>\d{2})([-_].+)?$"),
  re.compile(r"^(PXL|IMG|VID)_(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})_(?P<hour>\d{2})(?P<minute>\d{2})(?P<second>\d{2})(\d{3})?(\.LS|\.PORTRAIT(\~\d)?|\~\d|\~5)?$"),
]

  
def check_match(date_str):
    for rex in DATE_REGEX:
        m = rex.match(date_str)
        if m is None:
            continue
        int_dict = {key: int(value) for key, value in m.groupdict().items()}
        return datetime(**int_dict)

    raise ValueError(f"No match to regex {date_str}")
  

def string_to_timestamp(date_str):
    date = check_match(date_str) 
    formatted_date = date.strftime("%Y%m%d%H%M.%S")
    return formatted_date


def gather_files():
    globs = ["**/*.mp4", "**/*.AVI", "**/*.avi", "**/*.jpg", "**/*.jpeg", "**/*.JPG"]
    output = []
    for spec in globs:
        output += list(Path(".").glob(spec))
    return output


def touch(fname):
    timestamp = string_to_timestamp(fname.stem)
    cmd = f'touch -m -t {timestamp} "{fname}"'
    print(cmd)
    os.system(cmd)


def main():

    files = gather_files()
    for fname in files:
        touch(fname)


if __name__ == "__main__":
    main()
