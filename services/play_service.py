import random

import data.config as config
from data.album import AlbumInfo

from sqlalchemy.future import select
from data import db_session
from data.album_data import Album
from random import randint


me = config.my_data
# folder = 8
folder_id = 2162484


async def get_album_data(folder):
    async with db_session.create_async_session() as session:
        release_id_query = select(Album.release_id).filter(Album.folder == folder)
        results = await session.execute(release_id_query)

        release_id_results = results.all()
        total_count = len(release_id_results)

        random_result = randint(1, total_count)
        # print(total_count, random_result)

        album_id_query = select(Album).filter(Album.folder == folder)
        results = await session.execute(album_id_query)
        album_rows = results.all()
        # print("Album ID:", album_rows)

        for album_id in album_rows[random_result]:
            album_id = album_id.release_id
            # print(album_rows)

        for artist_name in me.release(album_id).artists:
            artist_count = 0

            artist_name = (
                me.release(album_id).artists[artist_count].name
            )

            artist_count += 1
            # print(artist_name)

            artist_id = me.release(album_id).artists[0].id

            try:
                artist_url = me.release(album_id).artists[0].url
            except me.exceptions.HTTPError:
                artist_url = None

        release_url = me.release(album_id).url
        release_title = me.release(album_id).title

        #        print("release title in service: , ", release_title)

        release_image_url = me.release(album_id).images[0]["uri"]
        #        print("release image url in service: , ", release_image_url)

        genres = me.release(album_id).genres
        album_release_date = me.release(album_id).year

        if me.release(album_id).master is not None:
            main_release_date = me.release(album_id).master.fetch("year")
        else:
            main_release_date = album_release_date

        track_title = []
        track_duration = []
        track_position = []

        for tracks in me.release(album_id).tracklist:
            track_title.append(tracks.title)
            track_duration.append(tracks.duration)
            track_position.append(tracks.position)

    album_info = AlbumInfo(
        album_id,
        release_url,
        artist_id,
        artist_name,
        release_title,
        artist_url,
        release_image_url,
        genres,
        # discogs_main_id,
        main_release_date,
        album_release_date,
        track_title,
        track_duration,
        track_position,
    )
    print(album_info)
    return album_info


       # print(album_id, artist_name, artist_url, genres, main_release_date)



