#!/usr/bin/env python3

import os
import sys
from pathlib import Path
from argparse import ArgumentParser



FFMPEG = 'ffmpeg -i "%s" -map 0:v -map 0:a:0 -map 0:a -map 0:s? -c:v copy -c:s copy -c:a copy -c:a:0 ac3 -disposition:a:0 default -disposition:a:1 0 "%s"'



def check_args():
    parser = ArgumentParser(prog="nodts", description="Remove Dolby DTS from video")
    parser.add_argument("filename")
    return parser



def main():
    parser = check_args()
    args = parser.parse_args()
    src_path = Path(args.filename)
    if not src_path.exists():
        sys.exit(f"Path {src_path} not found")
    dest_path = src_path.with_stem(src_path.stem + "_ac3")
    if dest_path.exists():
        sys.exit(f"Refusing to overwrite file {dest_path}")
    cmd = FFMPEG % (str(src_path), str(dest_path))    
    os.system(cmd)


if __name__ == "__main__":
    main()

