from starlette.requests import Request
from typing import List, Optional
from sqlalchemy.future import select
from data import db_session
from data.album_data import Album
from data.album import AlbumInfo

import data.config as config
from data.choose import ChooseInfo
from data.config import my_data

me = config.my_data


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

        genres = me.release(release_id).genres
        print("Genres: ", genres, type(genres))
        album_release_date = me.release(release_id).year

        if me.release(release_id).master is not None:
            main_release_date = me.release(release_id).master.fetch("year")
        else:
            main_release_date = album_release_date

        track_title = []
        track_duration = []
        track_position = []

        for tracks in me.release(release_id).tracklist:
            track_title.append(tracks.title)
            track_duration.append(tracks.duration)
            track_position.append(tracks.position)

        album_info = AlbumInfo(
            release_id,
            release_url,
            artist_id,
            artist_name,
            release_title,
            artist_url,
            release_image_url,
            genres,
            # discogs_main_id,
            main_release_date,
            album_release_year,
            track_title,
            track_duration,
            track_position,
            mb_id,
        )
        print("Album info: ", album_info, album_info.genres, type(album_info.genres))
        return album_info
