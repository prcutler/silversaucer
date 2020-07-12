import requests
import os
import silversaucer.data.config as config
import random

# Discogs API Url for different folders in a collection
discogs_url = config.discogs_url + "/users/" + config.discogs_user + "/collection/folders/"


# Get just full length vinyl records in my LP folder in my collection - replace your folder # in the response method
def get_lp_collection():
    response = requests.get(discogs_url + "2162484")

    record_json = response.json()
    lp_count = int(record_json["count"])
    random_lp = random.randint(0, lp_count)

    return random_lp


# Includes both 7" and EP folders
def get_ep_collection():
    pass


def get_cd_collection():
    pass


def get_tape_collection():
    pass


def randomize_record():
    pass
