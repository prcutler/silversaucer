from starlette.requests import Request
from typing import List, Optional
from sqlalchemy.future import select
from data import db_session
from data.album_data import Album
from data.album import AlbumInfo

import data.config as config
import pendulum


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

        mb_release_str = release_results.mb_release_date
        if mb_release_str is not None:
            mb_release_convert = pendulum.parse(mb_release_str)

            mb_release_date = mb_release_convert.to_formatted_date_string()
            print("MB Release Date: ", mb_release_date, type(mb_release_date))

        else:
            mb_release_date = None
            pass

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

        track_info = []
        for track in me.release(release_id).tracklist:
            track_info.append([track.position, track.title, track.duration])

        print("Track info: ", track_info)

        for tracks in me.release(release_id).tracklist:

            track_duration.append(tracks.duration)
            track_position.append(tracks.position)
            track_title.append(tracks.title)

            print("API Tracklist info: ", tracks.title, type(tracks.title))

        # track_title = me.release(release_id).tracklist.
        print("Track Title: ", track_title, type(track_title))

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
            track_info,
            mb_id,
            mb_release_date,
        )
        print("Album info: ", album_info, album_info.genres, type(album_info.genres))
        return album_info
