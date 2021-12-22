"""
This script modifies one or more images to provide gamma correciton
and error-diffusion dithering so they'll look a little better with the
Protomatter matrix library, which initially does not support gamma
correction on its own.

Requires PIL/Pillow

Syntax is:
python protomatter_dither.py X file1, file2, file3, ...

X is an optional argument -- if it's 8, images are output as 8-bit color-
paletted BMPs, otherwise 24-bit BMPs are output.

Input files can be images in any format that PIL/Pillow supports -- PNG,
JPEG, BMP and so forth. Output is always BMP (8- or 24-bit as described
above). Output filenames will have '-processed' appended, e.g. for input
foo.jpg, output will be foo-processed.bmp (and any existing file with
that name will be clobbered).

There's probably a better way to do this with ImageMagick, just sayin'.
"""

import math
import sys

from PIL import Image

GAMMA = 2.6


def process(filename, output_8_bit=False, passthrough=None):
    """Given a color image filename, load image and apply gamma correction
    and error-diffusion dithering while quantizing to 565 color
    resolution. If output_8_bit is True, image is reduced to 8-bit
    paletted mode after quantization/dithering. If passthrough (a list
    of 3-tuple RGB values) is provided, dithering won't be applied to
    colors in the provided list, they'll be quantized only (allows areas
    of the image to remain clean and dither-free). Writes a BMP file
    with the same name plus '-processed' and .BMP extension.
    """
    img = Image.open(filename).convert("RGB")
    err_next_pixel = (0, 0, 0)  # Error diffused to the right
    err_next_row = [(0, 0, 0) for _ in range(img.size[0])]  # " diffused down
    for row in range(img.size[1]):
        for column in range(img.size[0]):
            pixel = img.getpixel((column, row))
            want = (
                math.pow(pixel[0] / 255.0, GAMMA) * 31.0,  # Gamma and
                math.pow(pixel[1] / 255.0, GAMMA) * 63.0,  # quantize
                math.pow(pixel[2] / 255.0, GAMMA) * 31.0,
            )  # to 565 res
            if pixel in passthrough:  # In passthrough list?
                got = (
                    pixel[0] >> 3,  # Take color literally,
                    pixel[1] >> 2,  # though quantized
                    pixel[2] >> 3,
                )
            else:
                got = (
                    min(
                        max(
                            int(
                                err_next_pixel[0] * 0.5
                                + err_next_row[column][0] * 0.25  # Diffuse
                                + want[0]  # from
                                + 0.5
                            ),
                            0,
                        ),
                        31,
                    ),  # prior XY
                    min(
                        max(
                            int(
                                err_next_pixel[1] * 0.5
                                + err_next_row[column][1] * 0.25
                                + want[1]
                                + 0.5
                            ),
                            0,
                        ),
                        63,
                    ),
                    min(
                        max(
                            int(
                                err_next_pixel[2] * 0.5
                                + err_next_row[column][2] * 0.25
                                + want[2]
                                + 0.5
                            ),
                            0,
                        ),
                        31,
                    ),
                )
            err_next_pixel = (want[0] - got[0], want[1] - got[1], want[2] - got[2])
            err_next_row[column] = err_next_pixel
            rgb565 = (
                (got[0] << 3) | (got[0] >> 2),  # Quantized result
                (got[1] << 2) | (got[1] >> 4),  # after dither
                (got[2] << 3) | (got[2] >> 2),
            )
            img.putpixel((column, row), rgb565)  # Put pixel back in image

    if output_8_bit:
        img = img.convert("P", palette=Image.ADAPTIVE)

    img.save(filename.split(".")[0] + "-processed.bmp")


# This is a set of color values where error diffusion dithering won't be
# applied (is still calculated for subsequent pixels, but not applied).
# Here it's set up for primary colors, so these always appear unfettered
# in output images.
PASSTHROUGH = (
    (0, 0, 0),
    (255, 0, 0),
    (255, 255, 0),
    (0, 255, 0),
    (0, 255, 255),
    (0, 0, 255),
    (255, 0, 255),
    (255, 255, 255),
)

REDUCE = False  # Assume 24-bit BMP out unless otherwise specified

for ARG_NUM, FILENAME in enumerate(sys.argv):  # Each argument...
    if ARG_NUM == 0:
        continue  # Skip first argument; is program name
    if FILENAME == "8":
        REDUCE = True  # Output 8-bit palettized images
        continue
    process(FILENAME, REDUCE, PASSTHROUGH)
