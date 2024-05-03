#!/usr/bin/env python3

"""
    Generate and download a google takeout in zip form.  Get the largest files possible, e.g. 50GB.
    Run for each takeout file:
       ./takeout.py index <takeout file>

    For each file in the takeout archive, a hashed directory structure will be created.  So if the sha2 digest of
    the file is 0000111122223333444455556666, then index file path will be created as:
    ~/.google_takeout_checksums/0000/1111/2222/3333/4444/5555/6666
    This allows very fast lookup of a hash in the index (even faster than a DB).  When you want to check if a local
    file is in the takeout, simply generate the digest, and test for existence of the equivalent hashed directory path.

    Do this with:
       ./takeout.py query <media file>
    To scan a whole directory run:
       ./takeout.py query <directory>

    Results will be in the form of a shell script which you can execute to delete the duplicates.  The script only
    generates the script.  You should check some of the entries to make sure they actually are in Google Photos.
    The name is included as a comment.  Example output of the query command:

    # In Google as: Takeout/Google Photos/Photos from 2007/2007-04-20_19.16.56.jpg
    # /home/biff/.google_takeout_checksums/94a0/3e7b/0ebb/0e0f/5fdd/e15d/2f78/a150/aa18/f0c4/bf8d/bd92/262d/d49d/8fd2/3216
    # 94a03e7b0ebb0e0f5fdde15d2f78a150aa18f0c4bf8dbd92262dd49d8fd23216
    echo "removing file black_easy_disk_M_2GB/A727-65A5/2001 - Dec 07/13_Dec 2007/dscf0782.jpg, already in Google"
    rm "black_easy_disk_M_2GB/A727-65A5/2001 - Dec 07/13_Dec 2007/dscf0782.jpg"

    On indexing sometimes zip entry checksums don't match.  In this case you may way to try again or do another
    takeout to correct the problem.  When you are done with the index run:

       ./takeout.py purge

    This will remove all index files, in case you switch to a different Google account, or you delete a lot of
    photos and want to recreate the index from scratch.


"""


import shutil
import sys
import hashlib
from argparse import ArgumentParser
from pathlib import Path
import zipfile
import textwrap
import os


HOME = Path.home()
DOT_DIR = HOME / ".google_takeout_checksums"
FAILED_DIR = DOT_DIR / "FAILED"

MEDIA_EXTENSIONS = [".jpg", ".jpeg", ".tif", ".mp4", ".mov", ".avi", ".png"]
MEDIA_EXTENSIONS += [_.upper() for _ in MEDIA_EXTENSIONS]


def hash_of_stream(fp):
    sha256 = hashlib.sha256()
    for chunk in iter(lambda: fp.read(1000*1000), b""):
        sha256.update(chunk)
    return sha256.hexdigest()


def get_path_for_digest(digest):
    path = DOT_DIR
    parts = textwrap.wrap(digest, 4)
    for directory in parts:
        path /= directory
    return path


def create_directory_marker(digest, name):
    """Create a directory marker file, with hashed directory structure"""
    path = get_path_for_digest(digest)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as fp:
        fp.write(name)


def scan_takeout(takeout):
    """ Iterate the takeout tgz file"""
    failed = []
    with zipfile.ZipFile(takeout, "r") as zip_file:
        for member in zip_file.infolist():
            if not member.is_dir():
                with zip_file.open(member) as fp:
                    path = Path(member.filename)
                    ext = path.suffix
                    if ext == ".json":
                        continue
                    if ext not in MEDIA_EXTENSIONS:
                        print(path)
                    try:
                        digest = hash_of_stream(fp)
                        create_directory_marker(digest, member.filename)
                    except zipfile.BadZipFile as e:
                        failed.append(path)
                        print(e)
    return failed


def check_index_for(media):
    with media.open("rb") as fp:
        digest = hash_of_stream(fp)
        path = get_path_for_digest(digest)
    if path.exists():
        with path.open("r") as fp_index:
            txt = fp_index.read()
            print(f"# In Google as: {txt}")
            print(f"# {path}")
            print(f"# {digest}")
            print(f'echo "removing file {media}, already in Google"')
            print(f'rm "{media}"')


def check_args():
    parser = ArgumentParser(prog='takeout',
                            description="""Keep track of which files you already uploaded to Google Photos""")
    subparsers = parser.add_subparsers(dest='command', help='Sub-command help')
    scan = subparsers.add_parser("index", help="Create index of takeout files")
    scan.add_argument("file_path", nargs="+", help="Paths to takeout files")
    subparsers.add_parser("purge", help="Remove all file digests from the index")
    query = subparsers.add_parser("query", help="Check if files are found in the index")
    query.add_argument("file_path", help="Path to check against the index")
    return parser


def do_index(args):
    """Gather data for the index"""
    for path in args.file_path:
        takeout = Path(path).absolute()
        failed = scan_takeout(takeout)
        if failed:
            print("Extracting failed files in full....")
            for bad in failed:
                cmd = f'unzip "{takeout}" "{bad}" -d {FAILED_DIR}'
                print(cmd)
                os.system(cmd)


def do_purge():
    shutil.rmtree(DOT_DIR, ignore_errors=True)
    if DOT_DIR.exists():
        print(f"Purge failed, check {DOT_DIR} for errors")
    else:
        print(f"Files purged from {DOT_DIR}")


def walk_directory(directory, pattern="*"):
    for item in directory.glob(pattern):
        if item.is_file():
            ext = item.suffix
            if ext in MEDIA_EXTENSIONS:
                yield item
        if item.is_dir():
            yield from walk_directory(item, pattern)


def do_query(args):
    path = Path(args.file_path)
    if path.is_dir():
        for file in walk_directory(path):
            check_index_for(file)
    else:
        check_index_for(path)


def main():
    parser = check_args()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    args = parser.parse_args()

    if args.command == "index":
        do_index(args)
    elif args.command == "purge":
        do_purge()
    elif args.command == "query":
        do_query(args)


if __name__ == "__main__":
    main()
