from starlette.requests import Request
from typing import List, Optional
from sqlalchemy.future import select
from data import db_session
from data.album_data import Album

import data.config as config
from data.choose import ChooseInfo
from data.config import my_data


async def get_release_data(release_id):
    async with db_session.create_async_session() as session:
        query = select(Album).filter(Album.release_id == release_id)
        results = await session.execute(query)

        query_results = results.scalar_one_or_none()
        print("query_results: ", query_results)

        release_results = query_results
        print("Release results: ", release_results)

        # release_results.release_id = release_id
        release_url: Optional[str] = release_results.release_url
        artist_id: int = release_results.artist_id
        artist_url: Optional[str] = release_results.artist_url
        artist_name: Optional[str] = release_results.artist_name
        release_title: Optional[str] = release_results.release_title
        release_image_url: Optional[str] = release_results.release_image_url
        album_release_year: Optional[str] = release_results.album_release_year
        mb_id: Optional[str] = release_results.mb_id

        # await session.commit()

        album_info = Album(
            release_url=release_url,
            release_id=release_id,
            artist_id=artist_id,
            artist_url=artist_url,
            artist_name=artist_name,
            release_title=release_title,
            release_image_url=release_image_url,
            album_release_year=album_release_year,
            mb_id=mb_id
        )

        return album_info
