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

        album_id = [album_id.release_id for album_id in album_rows[random_result]]
        print("Album ID:", album_id, type(album_id))
        album_id = album_id[0]

 #       for album_id in album_rows[random_result]:
 #           album_id = album_id.release_id
 #           print("Album ID:", album_id, type(album_id))

        artist_id = [album_id.artist_id for album_id in album_rows[random_result]]
        artist_id = artist_id[0]

        name = [name.artist_name for name in album_rows[random_result]]
        artist_name = name[0]

        url = [url.artist_url for url in album_rows[random_result]]
        artist_url = url[0]

        title = [title.release_title for title in album_rows[random_result]]
        release_title = title[0]

        url = [url.release_url for url in album_rows[random_result]]
        release_url = url[0]

        image_url = [image_url.release_image_url for image_url in album_rows[random_result]]
        release_image_url = image_url[0]

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



