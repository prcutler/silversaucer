import random
from random import randint

import requests

import data.config as config
from data.album import AlbumInfo
from data.config import my_data
from data.single import SingleInfo

# Discogs API Url for different folders in a collection
folder_url = config.discogs_url + "users/" + config.discogs_user + "/collection/folders"

api_token = config.discogs_user_token

discogs_api = folder_url + "?=" + api_token


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

        album_info = AlbumInfo(
            release_id,
            release_url,
            artist_id,
            release_title,
            release_image_url,
            genres,
            # discogs_main_id,
            album_release_date,
        )
        # print("Genres: ", genres)
        return album_info

    def single_random_folder():
        get_single_random_folder = random.randint(1, 3)

        return get_single_random_folder
