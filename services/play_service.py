import random

import data.config as config
from data.album import AlbumInfo
from data.config import my_data
from data.single import SingleInfo


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

        artist_id = artist_name
        release_id = album_release_id
        release_url = release_data.release(release_id).url
        release_title = release_data.release(album_release_id).title
        release_image_url = release_data.release(album_release_id).images[0]["uri"]

        genres = release_data.release(album_release_id).genres
        album_release_date = release_data.release(album_release_id).year

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
            release_title,
            release_image_url,
            genres,
            # discogs_main_id,
            album_release_date,
            track_title,
            track_duration,
            track_position,
        )
        # print("Genres: ", genres)
        return album_info

    def single_random_folder():
        get_single_random_folder = random.randint(1, 3)

        return get_single_random_folder
