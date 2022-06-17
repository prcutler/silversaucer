from starlette.requests import Request
from typing import List, Optional
from sqlalchemy.future import select
from data import db_session
from data.album_data import Album
from data.today_data import TodayInfo

import data.config as config
import pendulum


me = config.my_data


async def get_today_list():

    today = pendulum.today()
    print("Today: ", today)

    search = str(today.month) + "-" + str(16)
    print("Search: ", search)

    async with db_session.create_async_session() as session:

        query = select(Album).filter(Album.mb_release_date)
        results = await session.execute(query)

        query_results = results.scalar()
        print("query_results: ", query_results)

        if query_results.mb_release_date[::-4] is search:
            print("Search results: ", query_results)

        release_results = query_results
        print("Release results: ", release_results)

        release_id = release_results.release_id
        release_url: Optional[str] = release_results.release_url
        artist_id: int = release_results.artist_id
        artist_url: Optional[str] = release_results.artist_url
        artist_name: Optional[str] = release_results.artist_name
        release_title: Optional[str] = release_results.release_title
        release_image_url: Optional[str] = release_results.release_image_url
        album_release_year: Optional[str] = release_results.album_release_year
        mb_id = release_results.mb_id
        mb_release_date = release_results.mb_release_date

        album_info = TodayInfo(
            release_id,
            release_url,
            artist_id,
            artist_name,
            release_title,
            artist_url,
            release_image_url,
            album_release_year,
            mb_id,
            mb_release_date
        )
        print("Album info: ", album_info, type(album_info))

        return album_info
