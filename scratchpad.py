from typing import Any

from data.api_json import JSONData
from data.album_data import Album
from data.release import Release
from sqlalchemy.future import select
from data import db_session
from data import config

import requests

import musicbrainzngs


musicbrainzngs.set_useragent(
    "silversaucer",
    "0.1",
    "https://github.com/prcutler/silversaucer/",)


mb_album_id = '52f218b7-7a2d-444a-b9bf-faaaa8175759'
artist_id = "c5c2ea1c-4bde-4f4d-bd0b-47b200bf99d6"

try:
    result = musicbrainzngs.get_artist_by_id(artist_id)
except WebServiceError as exc:
    print("Something went wrong with the request: %s" % exc)
else:
    artist = result["artist"]
    print("name:\t\t%s" % artist["name"])
    print("sort name:\t%s" % artist["sort-name"])

try:
    result = musicbrainzngs.get_release_by_id(mb_album_id)
except ReferenceError as exc:
    print("Something went wrong with the request: %s" % exc)
else:
    id = result['release']["id"]
    album = result['release']["title"]
    release_date = result['release']['date']
    # artist = result['release']["artist"]
    # print("name:\t\t%s" % artist["name"])
    # print("sort name:\t%s" % artist["sort-name"])
    print("MusicBrainz ID: ", id, "Album: ", album, "Release Date: ", release_date)


