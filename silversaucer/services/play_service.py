import random

import requests

import silversaucer.data.config as config

# Discogs API Url for different folders in a collection
folder_url = config.discogs_url + "users/" + config.discogs_user + "/collection/folders"

api_token = config.discogs_user_token


class RandomRecordService:
    # If you have not put your records into folders, use this method
    # Get just full length vinyl records in my LP folder in my collection - replace your folder # in the response method

    @staticmethod
    def get_folder_count(folder):

        discogs_api = folder_url + "?=" + api_token

        # TODO Add an if statement to check for a 200 or 404 response code and redirect on 404 to error page

        response = requests.get(discogs_api)

        record_json = response.json()

        json_data = record_json
        json_folders = json_data["folders"]

        # print(type(json_folders))
        # print(type(json_folders)["folders"])

        for get_folder_id in json_folders:

            if get_folder_id["id"] == folder:

                lp_count = get_folder_id["count"]

                random_lp = random.randint(1, lp_count)

                if 0 < random_lp <= 99:
                    page = "?page=1&per_page=100"

                elif 100 < random_lp <= 199:
                    page = "?page=2&per_page=100"

                elif 200 < random_lp <= 299:
                    page = "?page=3&per_page=100"

                elif 300 < random_lp <= 399:
                    page = "?page=4&per_page=100"

                elif 400 < random_lp <= 499:
                    page = "?page=5&per_page=100"

                elif 500 < random_lp <= 599:
                    page = "?page=6&per_page=100"

                elif 600 < random_lp <= 699:
                    page = "?page=7&per_page=100"

                elif 700 < random_lp <= 799:
                    page = "?page=8&per_page=100"

                elif 800 < random_lp <= 899:
                    page = "?page=0&per_page=100"

                else:
                    page = "?page=10&per_page=100"

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
            else:
                # print("You screwed up")
                pass

    @staticmethod
    def get_album_data(folder, album_release_id):

        release_api = (
            config.discogs_url
            + "releases/"
            + str(album_release_id[0])
            + "?"
            + config.discogs_user_token
        )

        response = requests.get(release_api)
        release_json = response.json()

        # If the folder is equal to the "full albums folder":
        if folder == 2162484:

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

            return {
                "release_title": release_title,
                "release_uri": release_uri,
                "artist_name": artist_name,
                "artist_url": artist_url,
                "release_date": release_date,
                "discogs_main_id": discogs_main_id,
                "discogs_main_url": discogs_main_url,
                "main_release_date": main_release_date,
                "release_image_uri": release_image_uri,
                "genres": genres,
            }

        else:
            # For all other folders:

            release_uri = release_json["uri"]
            artist_name = release_json["artists"][0]["name"]
            artist_url = release_json["artists"][0]["resource_url"]
            artist_id = release_json["artists"][0]["id"]
            release_date = release_json["released"]
            release_title = release_json["title"]
            main_release_date = release_json["year"]
            release_image_uri = release_json["images"][0]["uri"]
            genres = release_json["genres"]

            return {
                "release_title": release_title,
                "release_uri": release_uri,
                "artist_name": artist_name,
                "artist_url": artist_url,
                "release_date": release_date,
                "main_release_date": main_release_date,
                "release_image_uri": release_image_uri,
                "genres": genres,
            }


class GetMainReleaseDate:
    pass
