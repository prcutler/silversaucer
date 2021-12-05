import random
from random import *

import requests

import data.config as config
from data.album import AlbumInfo

# Discogs API Url for different folders in a collection
folder_url = config.discogs_url + "users/" + config.discogs_user + "/collection/folders"

api_token = config.discogs_user_token

discogs_api = folder_url + "?=" + api_token


class RandomRecordService:
    @staticmethod
    def get_folder_count(folder):

        # TODO Add an if statement to check for a 200 or 404 response code and redirect on 404 to error page
        response = requests.get(discogs_api)
        record_json = response.json()

        json_data = record_json
        json_folders = json_data["folders"]

        for get_folder_id in json_folders:
            if get_folder_id["id"] == folder:

                lp_count = get_folder_id["count"]

                random_lp = random.randint(0, lp_count)

                pg = (random_lp // 100) + 1
                page = "?page=" + str(pg) + "&per_page=100"

                position_string = str(random_lp)[1:]
                position = int(position_string) - 1

                random_album_api_call = (
                    folder_url + "/" + str(folder) + "/releases?" + page + api_token
                )
                response = requests.get(random_album_api_call)

                # Fix the pagination problem (sorting?)
                random_album_json = response.json()
                random_album_release_id = random_album_json["releases"][position]["id"]

                return random_album_release_id, folder

    @staticmethod
    def get_album_data(folder, album_release_id):

        release_api = (
            config.discogs_url
            + "releases/"
            #            + str(album_release_id[0])
            + str(album_release_id)
            + "?"
            + config.discogs_user_token
        )

        response = requests.get(release_api)
        release_json = response.json()

        # If the folder is equal to the "full albums folder":
        # if folder == 2162484:

        release_uri = release_json["uri"]
        artist_name = release_json["artists"][0]["name"]
        artist_url = release_json["artists"][0]["resource_url"]
        artist_id = release_json["artists"][0]["id"]
        release_date = release_json["released"]
        discogs_main_id = release_json["master_id"]
        discogs_main_url = release_json["master_url"]
        release_title = release_json["title"]
        main_release_date = release_json["year"]
        release_image_uri = release_json["images"][0]["uri"]
        genres = release_json["genres"]

        return AlbumInfo(
            release_uri,
            artist_name,
            artist_url,
            artist_id,
            release_date,
            discogs_main_id,
            discogs_main_url,
            release_title,
            main_release_date,
            release_image_uri,
            genres,
        )

        # "release_title": release_title,
        # "release_uri": release_uri,
        # "artist_name": artist_name,
        # "artist_url": artist_url,
        # "release_date": release_date,
        # "discogs_main_id": discogs_main_id,
        # "discogs_main_url": discogs_main_url,
        # "main_release_date": main_release_date,
        # "release_image_uri": release_image_uri,
        # "genres": genres,
        # }

        # else:
        # For all other folders:

        #    release_uri = release_json["uri"]
        #    artist_name = release_json["artists"][0]["name"]
        #    artist_url = release_json["artists"][0]["resource_url"]
        #    artist_id = release_json["artists"][0]["id"]
        #    release_date = release_json["released"]
        #    release_title = release_json["title"]
        #    main_release_date = release_json["year"]
        #    release_image_uri = release_json["images"][0]["uri"]
        #    genres = release_json["genres"]

        #   return {
        #       "release_title": release_title,
        #       "release_uri": release_uri,
        #       "artist_name": artist_name,
        #       "artist_url": artist_url,
        #       "release_date": release_date,
        #       "main_release_date": main_release_date,
        #       "release_image_uri": release_image_uri,
        #       "genres": genres,
        #   }

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

            pg = (random_lp // 100) + 1
            page = "?page=" + str(pg) + "&per_page=100"

            position_string = str(random_lp)[1:]
            position = int(position_string) - 1

            random_album_api_call = (
                folder_url + "/" + str(folder) + "/releases?" + page + api_token
            )
            response = requests.get(random_album_api_call)

            # Fix the pagination problem (sorting?)
            random_album_json = response.json()
            return random_album_json["releases"][position]["id"]
