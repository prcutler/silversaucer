from typing import Dict, Any

import data.config as config
from data.api_json import JSONData
from sqlalchemy.future import select
from data import db_session
from sqlalchemy import text


async def get_album_json() -> dict[str, Any]:
    #async with db_session.create_async_session() as session:
        #query = (
        #    select(JSONData.album)
        #    .filter(JSONData.id == 1))

#        results = await session.execute(query)
#        results_json = results.scalar_one_or_none()

##        album_json = {'album': results_json}
 #       print("album json: ", album_json)
 #       return album_json

    album_info = {'album': "Paul's Boutique"}
    return album_info

async def get_artist_json() -> dict[str, Any]:
    async with db_session.create_async_session() as session:
        query = (
            select(JSONData.artist)
            .filter(JSONData.id == 1))

        results = await session.execute(query)
        results_json = results.scalar_one_or_none()

        artist_json = {'artist': results_json}

        return artist_json


async def get_image_url_json() -> dict[str, Any]:
    async with db_session.create_async_session() as session:

        query = (select(JSONData.image_url).filter(JSONData.id == 1))

        results = await session.execute(query)
        image_url_json = results.scalar()
        print("image url: ", image_url_json, type(image_url_json))

        image_json = {'image': image_url_json}

        return image_json
