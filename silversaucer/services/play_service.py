import os
import random

import requests

import silversaucer.data.config as config

# Discogs API Url for different folders in a collection

# TODO Fix this URL call below - it's not requesting all the folders, needs authentication (only returns 0)
folder_url = config.discogs_url + "users/" + config.discogs_user + "/collection/folders"

release_url = (
    config.discogs_url + "users/" + config.discogs_user + "/collection/folders"
)

api_token = config.discogs_user_token

print(folder_url)
# If you have not put your records into folders, use all_discogs or enter the folder ID for your folders below
# (I have created folders for each type in my collection)


class RandomRecordService:

    # TODO This could maybe be refactored into a method that passes it

    # If you have not put your records into folders, use this method
    # Get just full length vinyl records in my LP folder in my collection - replace your folder # in the response method

    @staticmethod
    def get_folder_count(folder):

        discogs_api = folder_url + "?=" + api_token

        # TODO Add an if statement to check for a 200 or 404 response code and redirect on 404 to error page

        response = requests.get(discogs_api)
        print(folder)
        print(response)

        all_folder = 0
        lp_folder = 2162484
        twelve_inch_folder = 2198941
        ten_inch_folder = 2162486
        seven_inch_folder = 2162483
        cd_folder = 2162488
        tape_folder = 2162487
        digital_folder = 2198943

        # TODO The folder is hardcoded below (8) - could loop through the JSON to match and make it a variable
        record_json = response.json()

        json_data = record_json
        json_folders = json_data["folders"]

        print(type(json_folders))
        print(type(json_folders)["folders"])
        #        print(type(json_folders.keys), json_folders.keys())
        #        print(type(json_folders.values), json_folders.values())

        for get_folder_id in json_folders:
            print(json_folders)
            print(len(json_folders))
            for index in range(len(json_folders)):
                if folder == json_folders[index]:
                    # print("Folder passed = ", folder, "Folder ID =", folder_id)
                    # folder_test = 2162484
                    print(folder)
                    lp_count = get_folder_id.values()
                    # lp_count = int(record_json["folders"][folder_id]["count"])
                    print(lp_count)
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
                    print(position)

                    random_album_api_call = (
                        folder_url
                        + "/"
                        + str(lp_folder)
                        + "/releases?"
                        + page
                        + api_token
                    )
                    response = requests.get(random_album_api_call)

                    # Fix the pagination problem (sorting?)
                    random_album_json = response.json()
                    random_album_release_id = random_album_json["releases"][position][
                        "id"
                    ]
                    print(random_album_release_id)

                    return random_album_release_id
                else:
                    print("You screwed up")

    @staticmethod
    def get_ep_collection():

        random_folder = random.randint(0, 2)

        if random_folder == 0:
            response = requests.get(folder_url + twelve_inch_folder)

            record_json = response.json()
            ep_count = int(record_json["count"])
            random_ep = random.randint(1, ep_count)

        elif random_folder == 1:
            response = requests.get(folder_url + ten_inch_folder)

            record_json = response.json()
            ep_count = int(record_json["count"])
            random_ep = random.randint(1, ep_count)

        else:
            response = requests.get(folder_url + seven_inch_folder)

            record_json = response.json()
            ep_count = int(record_json["count"])
            random_ep = random.randint(1, ep_count)

        return random_ep

    @staticmethod
    def get_cd_collection():
        pass

    @staticmethod
    def get_tape_collection():
        pass

    @staticmethod
    def get_album_data(album_release_id):
        release_api = (
            config.discogs_url
            + "releases/"
            + str(album_release_id)
            + "?"
            + config.discogs_user_token
        )
        print(release_api)
        response = requests.get(release_api)
        print(response)

        release_json = response.json()

        # Get the main release

        # Pass the main release

        # Get the release date of the first album in the main release's list

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

        print(
            release_title,
            release_uri,
            artist_name,
            artist_id,
            artist_url,
            release_date,
            discogs_main_id,
            discogs_main_url,
            main_release_date,
            release_image_uri,
            genres,
        )

        return (
            release_title,
            artist_name,
            artist_url,
            release_date,
            discogs_main_id,
            discogs_main_url,
            main_release_date,
            release_image_uri,
            genres,
        )


class GetMainReleaseDate:
    pass
