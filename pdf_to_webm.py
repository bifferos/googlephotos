#!/usr/bin/env python3

"""
    PDF files cannot be uploaded to Google photos but with the help of Poppler and ffmpeg you can convert them into
    a video file.  From experimentation, a 4 seconds pause on each page seems to give the best results.

    webm and vp9 has the advantage of not caring about resolution, so there's no need for any scaling
    if pdftoppm happens to output an invalid h264 resolution.  Otherwise we could have used mp4.  webm is popular
    enough and played by most things, however.

    I consider 300dpi is going to be more than good enough to see everything because that's my printer resolution.
    I don't have many PDF files, so optimising for space is no big deal but this could be reduced.
"""


import tempfile
import shutil
import os
import re
from pathlib import Path
from subprocess import run
from datetime import datetime
from dateutil import parser


PDF_INFO_REX = re.compile(r"^([^:]+): +([^ ].*)")


def pdf_info_to_dict(info_string):
    out = {}
    for line in info_string.split("\n"):
        text = line.strip()
        match = PDF_INFO_REX.match(text)
        if match is None:
            continue
        key = match.group(1)
        value = match.group(2)
        out[key] = value
    return out


def date_from_pdf_info(info_string):
    date_string = pdf_info_to_dict(info_string)["CreationDate"]
    datetime_obj = parser.parse(date_string)
    ts = datetime_obj.timestamp()
    return ts


def page_count_from_pdf_info(info_string):
    return int(pdf_info_to_dict(info_string)["Pages"])


class PdfConverterContext:
    """Context management of the conversion, cleaning up after"""
    def __init__(self, pdf_name):
        self.pdf_name = pdf_name
        self._temp_dir = None

    def exec(self, args):
        result = run(args, cwd=self._temp_dir,
                     capture_output=True, text=True)
        print("OUT:", result.stdout)
        print("ERR:", result.stderr)
        return result.stdout

    def convert(self):
        pdf_info = self.exec(["pdfinfo", "-isodates", self.pdf_name])
        pages = page_count_from_pdf_info(pdf_info)
        self.exec(["pdftoppm", "-png", "-r", "300", self.pdf_name, "png"])
        output = None

        if pages == 1:
            # Special case a single page, just turn it into a PNG
            output = self.pdf_name.with_suffix(".png")
            png_path = Path(self._temp_dir) / "png-1.png"
            shutil.copy(png_path, output)
        else:
            output = self.pdf_name.with_suffix(".webm")
            self.exec(["ffmpeg", "-y", "-framerate", "0.25", "-i", "png-%d.png", "-c:v", "libvpx-vp9",
                       "-r", "0.25", "-pix_fmt", "yuv420p", output])
        timestamp = date_from_pdf_info(pdf_info)
        os.utime(output, (timestamp, timestamp))

    def __enter__(self):
        self._temp_dir = tempfile.mkdtemp(prefix="pdf_to_webm_")
        print(f"Created tmpdir {self._temp_dir}")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._temp_dir and os.path.exists(self._temp_dir):
            shutil.rmtree(self._temp_dir)


def main():
    here = Path(".").resolve()
    for pdf in here.glob("*.pdf"):
        with PdfConverterContext(pdf) as converter:
            converter.convert()


if __name__ == "__main__":
    main()

