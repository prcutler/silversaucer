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


mb_album_id = 'db5676ca-f922-4ec1-87bf-35b60d71e126'


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


