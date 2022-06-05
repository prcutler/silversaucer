import random

import data.config as config
from data.album import AlbumInfo
from data.config import my_data

from sqlalchemy.future import select
from data import db_session
from data.album_data import Album
from random import randint


me = config.my_data
folder = 8
folder_id = 2162484


async def get_album_data():
    async with db_session.create_async_session() as session:
        release_id_query = select(Album.release_id)
        results = await session.execute(release_id_query)

        release_id_results = results.all()
        total_count = len(release_id_results)

        album_pick = randint(1, total_count)
        print(total_count, album_pick)

        album_id_query = select(Album.release_id).filter(Album.id == album_pick)

        results = await session.execute(album_id_query)

        album_id = results.scalar_one_or_none()

        artist_count = 0
        for artist_name in me.release(album_id).artists:
            artist_name = (
                me.release(album_id).artists[artist_count].name
            )

            artist_count += 1
            print(artist_name)

        artist_id = me.release(album_id).artists[0].id
        artist_url = me.release(album_id).artists[0].url

        release_url = me.release(album_id).url
        release_title = me.release(album_id).title

        #        print("release title in service: , ", release_title)

        release_image_url = me.release(album_id).images[0]["uri"]
        #        print("release image url in service: , ", release_image_url)

        genres = me.release(album_id).genres
        album_release_date = me.release(album_id).year

        main_release_date = me.release(album_id).master.fetch("year")
        if main_release_date == 0:
            main_release_date = album_release_date
        else:
            main_release_date = main_release_date

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
    print(album_info, album_info.release_title)
    return album_info


       # print(album_id, artist_name, artist_url, genres, main_release_date)


class RandomRecordService:
    @staticmethod
    def get_folder_count2(folder):

        # print(folder)
        lp_count = len(my_data.identity().collection_folders[folder].releases)
        # print(lp_count)

        random_lp = random.randint(0, lp_count)
        # print("Random # = ", random_lp)

        random_album_release_id = (
            my_data.identity().collection_folders[folder].releases[random_lp].release.id
        )
        # print("Random_ID = ", random_album_release_id)

        return random_album_release_id

    @staticmethod
    def get_album_data(album_release_id):

        release_data = config.my_data

        artist_count = 0

        for artist_name in release_data.release(album_release_id).artists:
            artist_name = (
                release_data.release(album_release_id).artists[artist_count].name
            )

            artist_count += 1
            # print(artist_name)

        artist_id = release_data.release(album_release_id).artists[0].name
        artist_url = release_data.release(album_release_id).artists[0].url

        release_id = album_release_id
        release_url = release_data.release(release_id).url
        release_title = release_data.release(album_release_id).title

        #        print("release title in service: , ", release_title)

        release_image_url = release_data.release(album_release_id).images[0]["uri"]
        #        print("release image url in service: , ", release_image_url)

        genres = release_data.release(album_release_id).genres
        album_release_date = release_data.release(album_release_id).year

        main_release_date = release_data.release(album_release_id).master.fetch("year")
        if main_release_date == 0:
            main_release_date = album_release_date
        else:
            main_release_date = main_release_date

        track_title = []
        track_duration = []
        track_position = []

        for tracks in release_data.release(album_release_id).tracklist:
            track_title.append(tracks.title)
            track_duration.append(tracks.duration)
            track_position.append(tracks.position)
            # print(track_title, type(track_title))

        #        tracklist = release_data.release(album_release_id).tracklist.title
        #        print(tracklist)

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
            album_release_date,
            track_title,
            track_duration,
            track_position,
        )
        #        print("release title in album_info: ", album_info.release_title)

        print(
            album_info.artist_name,
            album_info.release_id,
            album_info.release_title,
            # album_info.release_image_url,
            # album_info.genres,
            # album_info.album_release_date,
            # album_info.main_release_date,
            # album_info.track_title,
            # album_info.track_duration,
            # album_info.track_position
        )

        return album_info

    @staticmethod
    def single_random_folder():
        get_single_random_folder = random.randint(1, 3)

        return get_single_random_folder
