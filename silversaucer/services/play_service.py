import requests
import os
import silversaucer.data.config as config
import random

# Discogs API Url for different folders in a collection
discogs_url = config.discogs_url + "/users/" + config.discogs_user + "/collection/folders/"

# If you have not put your records into folders, use all_discogs or enter the folder ID for your folders below
# (I have created folders for each type in my collection)

all_discogs = "/0/"
lp_folder = "/2162484/"
twelve_inch_folder = "/2198941/"
ten_inch_folder = "/2162486/"
seven_inch_folder = "/2162483/"
cd_folder = "/2162488/"
tape_folder = "/2162487/"
digital_folder = "/2198943/"


# If you have not put your records into folders, use this method
def get_all_collection():
    response = requests.get(discogs_url + all_discogs)

    record_json = response.json()
    all_count = int(record_json["count"])
    random_record = random.randint(1, all_count)

    return random_record


# Get just full length vinyl records in my LP folder in my collection - replace your folder # in the response method
def get_lp_collection():
    response = requests.get(discogs_url + lp_folder)

    record_json = response.json()
    lp_count = int(record_json["count"])
    random_lp = random.randint(0, lp_count)

    return random_lp


# Includes 7", 12 and EP folders
def get_ep_collection():

    random_folder = random.randint(0, 2)

    if random_folder == 0:
        response = requests.get(discogs_url + twelve_inch_folder)

        record_json = response.json()
        ep_count = int(record_json["count"])
        random_ep = random.randint(1, ep_count)

    elif random_folder == 1:
        response = requests.get(discogs_url + ten_inch_folder)

        record_json = response.json()
        ep_count = int(record_json["count"])
        random_ep = random.randint(1, ep_count)

    else:
        response = requests.get(discogs_url + seven_inch_folder)

        record_json = response.json()
        ep_count = int(record_json["count"])
        random_ep = random.randint(1, ep_count)

    return random_ep


def get_cd_collection():
    pass


def get_tape_collection():
    pass


