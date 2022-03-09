from typing import Dict, Any

import data.config as config
from data.api_json import JSONData
from sqlalchemy.future import select
from data import db_session
from services import api_service


async def get_album_json() -> dict[str, Any]:
    async with db_session.create_async_session() as session:
        query = (select(JSONData.album).filter(JSONData.id == 1))

        results = await session.execute(query)
        album_json = results.scalar()

        return album_json


async def get_artist_json() -> dict[str, Any]:
    async with db_session.create_async_session() as session:
        query = (
            select(JSONData.artist)
            .filter(JSONData.id == 1))

        results = await session.execute(query)
        results_json = results.scalar_one_or_none()

        # artist_json = {'artist': results_json}

        return results_json


async def get_image_url_json() -> dict[str, Any]:
    async with db_session.create_async_session() as session:

        query = (select(JSONData.image_url).filter(JSONData.id == 1))

        results = await session.execute(query)
        image_url_json = results.scalar()

        return image_url_json


async def update_api_db(album, artist, image_url):
    async with db_session.create_async_session() as session:
        #session.add(json_data)
        #await session.commit()

        query = select(JSONData).filter(JSONData.id == 1)
        results = await session.execute(query)

        api_data = results.scalar()

        api_data.album = album
        api_data.artist = artist
        api_data.image_url = image_url

        await session.commit()



