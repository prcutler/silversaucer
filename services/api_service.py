from typing import Any

from data.api_json import JSONData
from sqlalchemy.future import select
from data import db_session
from data import config
from Adafruit_IO import Client, Feed
import urllib3
from PIL import Image
import math

import urllib.request

import paho.mqtt.client as mqtt


async def get_album_json() -> dict[str, Any]:
    async with db_session.create_async_session() as session:
        query = select(JSONData.album).filter(JSONData.id == 1)

        results = await session.execute(query)
        album_json = results.scalar()

        return album_json


async def get_artist_json() -> dict[str, Any]:
    async with db_session.create_async_session() as session:
        query = select(JSONData.artist).filter(JSONData.id == 1)

        results = await session.execute(query)
        results_json = results.scalar_one_or_none()

        # artist_json = {'artist': results_json}

        return results_json


async def get_image_url_json() -> dict[str, Any]:
    async with db_session.create_async_session() as session:

        query = select(JSONData.image_url).filter(JSONData.id == 1)

        results = await session.execute(query)
        image_url_json = results.scalar()

        return image_url_json


async def update_api_db(album, artist, image_url):
    async with db_session.create_async_session() as session:

        query = select(JSONData).filter(JSONData.id == 1)
        results = await session.execute(query)

        api_data = results.scalar()

        try:
            api_data.album = album
            api_data.artist = artist
            api_data.image_url = image_url
            await session.commit()

        except AttributeError:

            api_data = JSONData(album=album, artist=artist, image_url=image_url)
            session.add(api_data)
            await session.commit()


async def get_discogs_image(release_image_url):
    print(release_image_url)
#    image_dl = requests.get(release_image_url, stream=True).raw

#    r = requests.get(release_image_url, stream=True)

#    with open("static/img/album-art/image_600.jpg", "wb") as f:
#       for chunk in r.iter_content(chunk_size=16*1024):
#            f.write(chunk)

    # urllib.request.urlretrieve(release_image_url, "static/img/album-art/image_600.jpg")
    # urllib.request.urlretrieve(release_image_url + config.discogs_user_token, "static/img/album-art/image_600.jpg")

    http = urllib3.PoolManager()
    response = http.request('GET', release_image_url)
    with open('static/img/album-art/image_600.jpg', 'wb') as file:
        file.write(response.data)

    download = Image.open("static/img/album-art/image_600.jpg")
#    download = Image.open(image_dl)
    download.save("static/img/album-art/image_600.jpg")

    img = Image.open("static/img/album-art/image_600.jpg")
    img.quantize(colors=16, method=2)
    smol_img = img.resize((320, 320))
    convert = smol_img.convert(mode="P", palette=Image.WEB)
    convert.save("static/img/album-art/image_300.bmp")

    img = Image.open("static/img/album-art/image_600.jpg")
    img.quantize(colors=16, method=2)
    size64 = img.resize((64, 64))
    convert64 = size64.convert(mode="P", palette=Image.ADAPTIVE)
    convert64.save("static/img/album-art/image64.bmp")

    img = Image.open("static/img/album-art/image_600.jpg")
    size480 = img.resize((480, 480))
    size480.save("static/img/album-art/image480.jpg")

    img = Image.open("static/img/album-art/image_600.jpg")
    img.quantize(colors=16, method=2)
    size480bmp = img.resize((480, 480))
    convert480bmp = size480bmp.convert(mode="P", palette=Image.ADAPTIVE)
    convert480bmp.save("static/img/album-art/480.bmp")


GAMMA = 2.6


async def process_image():
    """Given a color image filename, load image and apply gamma correction
       and error-diffusion dithering while quantizing to 565 color
       resolution. If output_8_bit is True, image is reduced to 8-bit
       paletted mode after quantization/dithering. If passthrough (a list
       of 3-tuple RGB values) is provided, dithering won't be applied to
       colors in the provided list, they'll be quantized only (allows areas
       of the image to remain clean and dither-free). Writes a BMP file
       with the same name plus '-processed' and .BMP extension.
    """

    # print(filename, output_8_bit, passthrough)
    img = Image.open('static/img/album-art/image64.bmp').convert('RGB')
    # img.show()
    # print(img.format, img.size, img.mode)
    err_next_pixel = (0, 0, 0) # Error diffused to the right
    err_next_row = [(0, 0, 0) for _ in range(img.size[0])] # " diffused down
    # print(err_next_row)

    # This is a set of color values where error diffusion dithering won't be
    # applied (is still calculated for subsequent pixels, but not applied).
    # Here it's set up for primary colors, so these always appear unfettered
    # in output images.
    passthrough = ((0, 0, 0),
                   (255, 0, 0),
                   (255, 255, 0),
                   (0, 255, 0),
                   (0, 255, 255),
                   (0, 0, 255),
                   (255, 0, 255),
                   (255, 255, 255))

    REDUCE = True  # Assume 8-bit BMP out unless otherwise specified

    for row in range(img.size[1]):
        # print(img.size)
        for column in range(img.size[0]):
            pixel = img.getpixel((column, row))
            want = (math.pow(pixel[0] / 255.0, GAMMA) * 31.0,  # Gamma and
                    math.pow(pixel[1] / 255.0, GAMMA) * 63.0,  # quantize
                    math.pow(pixel[2] / 255.0, GAMMA) * 31.0)  # to 565 res
            if pixel in passthrough:  # In passthrough list?
                got = (pixel[0] >> 3,  # Take color literally,
                       pixel[1] >> 2,  # though quantized
                       pixel[2] >> 3)
            else:
                got = (min(max(int(err_next_pixel[0] * 0.5 +  # Diffuse
                                   err_next_row[column][0] * 0.25 +  # from
                                   want[0] + 0.5), 0), 31),  # prior XY
                       min(max(int(err_next_pixel[1] * 0.5 +
                                   err_next_row[column][1] * 0.25 +
                                   want[1] + 0.5), 0), 63),
                       min(max(int(err_next_pixel[2] * 0.5 +
                                   err_next_row[column][2] * 0.25 +
                                   want[2] + 0.5), 0), 31))
            err_next_pixel = (want[0] - got[0],
                              want[1] - got[1],
                              want[2] - got[2])
            err_next_row[column] = err_next_pixel
            rgb565 = ((got[0] << 3) | (got[0] >> 2),  # Quantized result
                      (got[1] << 2) | (got[1] >> 4),  # after dither
                      (got[2] << 3) | (got[2] >> 2))
            img.putpixel((column, row), rgb565)  # Put pixel back in image

    img = img.convert('P', palette=Image.ADAPTIVE)

    img.save('static/img/album-art/image64p.bmp')


async def publish_image():

    aio = Client(config.aio_username, config.aio_key)
    aio.send_data('albumart', "New album picked!")
