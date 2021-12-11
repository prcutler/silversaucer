import random
from random import randint

import discogs_client
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
    def get_folder_count2():
        lp_count = len(my_data.identity().collection_folders[8].releases)
        # print(lp_count)

        random_lp = random.randint(0, lp_count)
        # print("Random # = ", random_lp)

        random_album_release_id = (
            my_data.identity().collection_folders[8].releases[random_lp].release.id
        )
        # print("Random_ID = ", random_album_release_id)

        return random_album_release_id

    @staticmethod
    def get_album_data(album_release_id):

        d = my_data.identity()

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

    def get_album_id():
        folder = 2162484
        RandomRecordService.get_folder_count(folder)

        response = requests.get(discogs_api)
        record_json = response.json()

        json_data = record_json
        json_folders = json_data["folders"]

        for get_folder_id in json_folders:
            lp_count = get_folder_id["count"]
            randint = random.randint(0, lp_count)

            random_lp = random.randint(0, lp_count)
            print(random_lp)

            random_album_api_call = (
                folder_url + "/" + str(folder) + "/releases?" + page + api_token
            )
            response = requests.get(random_album_api_call)

            # Fix the pagination problem (sorting?)
            random_album_json = response.json()
            album_id = random_album_json["releases"][position]["id"]

            return album_id

    def get_single_data():
        random_folder = randint(0, 2)

        if random_folder == 0:
            single = 2162483
        elif random_folder == 1:
            single = 2162486
        else:
            single = 2198941

        folder = single
        response = requests.get(discogs_api)
        record_json = response.json()

        json_data = record_json
        json_folders = json_data["folders"]
        for get_folder_id in json_folders:
            if get_folder_id["id"] == folder:

                single_count = get_folder_id["count"]

                random_single = random.randint(0, single_count)
                print(random_single)

                pg = (random_single // 100) + 1
                page = "?page=" + str(pg) + "&per_page=100"

                try:
                    position_string = str(random_single)[1:]
                    position = int(position_string) - 1
                    print(
                        "Position string",
                        position_string,
                        type(position_string),
                        "Position",
                        position,
                        type(position),
                    )
                except ValueError:
                    print("Value Error Time!")
                    get_position_numbers = position_string.translate(
                        None, position_string.letters
                    )
                    position = int(get_position_numbers) - 1

                random_single_api_call = (
                    folder_url + "/" + str(folder) + "/releases?" + page + api_token
                )
                response = requests.get(random_single_api_call)
                print(random_single_api_call)

                # Fix the pagination problem (sorting?)
                random_album_json = response.json()
                random_album_release_id = random_album_json["releases"][position]["id"]

                release_api = (
                    config.discogs_url
                    + "releases/"
                    + str(random_album_release_id)
                    + "?"
                    + config.discogs_user_token
                )

                print("Single Data Release API: ", release_api)
                response = requests.get(release_api)
                print(response)
                release_json = response.json()

                release_id = release_json["id"]
                release_uri = release_json["uri"]
                artist_id = release_json["artists"][0]["id"]
                release_title = release_json["title"]
                artist_name = release_json["artists"][0]["name"]
                artist_url = release_json["artists"][0]["resource_url"]
                release_image_uri = release_json["images"][0]["uri"]
                genres = release_json["genres"]
                album_release_date = release_json["released"]
                main_release_date = release_json["year"]

                print(release_image_uri[0], genres)

                single_info = SingleInfo(
                    release_id,
                    release_uri,
                    artist_id,
                    release_title,
                    artist_name,
                    artist_url,
                    release_image_uri,
                    genres,
                    album_release_date,
                    main_release_date,
                )

                print(
                    "Album Info: ",
                    single_info,
                    type(single_info),
                    single_info.artist_name,
                )
                print("Genres: ", genres)
                return single_info
