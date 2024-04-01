#!/usr/bin/env python3

import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


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
        still = here / ".wav_to_mp4_temp_image.png"
        text_to_image(f"{wav.parent}\n{wav.stem}", still)
        output = wav.with_suffix(".mp4")
        os.system(f'ffmpeg -loop 1 -i "{still}" -i {wav} -c:v libx264 -c:a alac -shortest "{output}"')


if __name__ == "__main__":
    main()

