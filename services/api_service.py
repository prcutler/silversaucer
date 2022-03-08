import data.config as config
from data.api_json import JSONData
from sqlalchemy.future import select
from data import db_session
from sqlalchemy import text


async def get_album_json() -> JSONData:
    async with db_session.create_async_session() as session:
        query = (
            select(JSONData)
            .filter(JSONData.id == 1).filter(JSONData.album))

        results = await session.execute(query)
        album_json = results.scalar_one_or_none()
        # print("Episodes: ", episodes, type(episodes))

        return album_json()


async def get_image_url_json() -> JSONData:
    async with db_session.create_async_session() as session:
        query = (
            select(JSONData)
            .filter(JSONData.id == 1).filter(JSONData.image_url))

        results = await session.execute(query)
        image_url_json = results.scalar_one_or_none()

        return image_url_json()


async def get_artist_json() -> JSONData:
    async with db_session.create_async_session() as session:
        query = (
            select(JSONData)
            .filter(JSONData.id == 1).filter(JSONData.artist))

        results = await session.execute(query)
        artist_json = results.scalar_one_or_none()

        return artist_json()