#!/usr/bin/env python3

"""
    WAV files cannot be uploaded to Google photos but with the help of ffmpeg and PIL you can convert them into
    a video file with an image that shows the name of the WAV.  Such mp4 files don't take up any extra space because
    the alac codec makes them smaller to offset the extra space used by the video track.  The video track is just a
    repeating image, so highly compressed as well.

    This script converts all .wav files in the current directory into mp4 files.

"""


import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap


def text_to_image(text, fname):
    image = Image.new('RGB', (640, 480), color='black')
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
    font = ImageFont.truetype(font_path, size=24)
    text_width, text_height = ImageDraw.Draw(image).textsize(text, font=font)
    text_x = (image.width - text_width) // 2
    text_y = (image.height - text_height) // 2
    draw = ImageDraw.Draw(image)
    draw.text((text_x, text_y), text, font=font, fill='yellow')
    image.save(fname)


def main():
    here = Path(".").resolve()
    for wav in here.glob("*.wav"):
        still = here / ".wav_to_google_temp_image.png"
        new_path = "\n".join(wav.parts[-5:])
        text_to_image(new_path, still)
        output = wav.with_suffix(".mp4")
        os.system(f'ffmpeg -loop 1 -i "{still}" -i "{wav}" -c:v libx264 -c:a alac -shortest "{output}"')
        timestamp = os.stat(wav).st_mtime
        os.utime(output, (timestamp, timestamp))


if __name__ == "__main__":
    main()

