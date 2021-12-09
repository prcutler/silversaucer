import fastapi
import requests
from fastapi_chameleon import template
from starlette import status
from starlette.requests import Request

import data.config as config

# Discogs API Url for different folders in a collection
folder_url = config.discogs_url + "users/" + config.discogs_user + "/collection/folders"

api_token = config.discogs_user_token

discogs_api = folder_url + "?=" + api_token

response = requests.get(discogs_api)
record_json = response.json()

json_data = record_json
json_folders = json_data["folders"]


class ChooseService:
    def get_folder_name_list():

        for get_folder_name in json_folders:
            folder_name = get_folder_name["name"]

        return folder_name

    def get_folder_id_list():

        for get_folder_id in json_folders:
            folder_id = get_folder_id["id"]

        return folder_id

    def get_artist_list(folder_id):
        for get_artist_id in json_folders:

            artist_id = json_folders["id"]

    def get_artist_names(folder_id):
        for get_album_id in json_folders:

            artist_names = json_folders["artists"]["name"]

            return artist_names

    def get_album_names(folder_id):
        for get_album_id in json_folders:

            album_names = json_folders["title"]

            return album_names
