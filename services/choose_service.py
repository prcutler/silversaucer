import json

import fastapi
import requests
from fastapi_chameleon import template
from starlette import status
from starlette.requests import Request

import data.config as config

# Discogs API Url for different folders in a collection
folder_url = config.discogs_url + "users/" + config.discogs_user + "/collection/folders"

api_token = config.discogs_user_token


# Get Folder Data and API call
folder_api = folder_url + "?=" + api_token

response = requests.get(folder_api)
folder_json = response.json()

folder_data = folder_json
json_folders = folder_data["folders"]

# Get Album Data and API Call
album_json = folder_url + "/" + str(2162484) + "/releases?" + api_token
album_response = requests.get(album_json)
album_json = album_response.json()


class ChooseService:
    def get_folder_name_list():

        for get_folder_name in json_folders:
            folder_name = get_folder_name["name"]
            # print("folder name: ", folder_name)

        return folder_name

    def get_folder_id_list():

        folder_id_list = []

        for get_folder_id in json_folders:
            folder_id = get_folder_id["id"]
            print("folder id: ", folder_id)

            folder_id_list.append(folder_id)
            print(folder_id_list)

            return folder_id_list

    def get_album_id_list():

        artist_counter = 0

        for get_artist_id in album_json["releases"]:
            artist_id = album_json["releases"][artist_counter]
            artist_counter += 1
            print(artist_id)

            print("Artist ID: ", artist_id)
            return artist_id

    def get_album_id():

        album_counter = 0

        for get_album_id in album_json["releases"]:
            album_id = album_json["releases"][album_counter]["id"]
            album_counter += 1
            print("album id: ", album_id)

        return album_id

    def get_artist_names():

        artist_names = album_json["artists"]["name"]
        print(artist_names)

        return artist_names

    def get_album_names():

        pass

        # album_names = json_folders["title"]

        # return album_names
