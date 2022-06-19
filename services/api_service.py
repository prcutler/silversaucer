from typing import Any

from data.api_json import JSONData
from sqlalchemy.future import select
from data import db_session
from data import config

from PIL import Image

import requests

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
    image_dl = requests.get(release_image_url, stream=True).raw
    download = Image.open(image_dl)
    download.save("static/img/album-art/image_600.jpg")

    img = Image.open("static/img/album-art/image_600.jpg")
    img.quantize(colors=16, method=2)
    smol_img = img.resize((320, 320))
    convert = smol_img.convert(mode="P", palette=Image.WEB)
    convert.save("static/img/album-art/image_300.bmp")


async def publish_image(image_url):
    client = mqtt.Client()
    client.username_pw_set(config.mqtt_user, config.mqtt_pw)
    client.connect("mqtt.silversaucer.com", 1883)
    client.publish("albumart", "Ping!")
    client.disconnect()
