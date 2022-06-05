from typing import Any

from data.api_json import JSONData
from data.album_data import Album
from sqlalchemy.future import select
from data import db_session
from data import config

import requests


me = config.my_data.identity()
print(me)

folder = 2162484
x = 0

print("Me.collection_folders: ", me.collection_folders)

# for item in me.collection_folders[8].releases:
#    print(item)

for records in me.collection_folders[0].releases:
    release_id = records.release.id
    release_url = records.release.url
    artist_id = records.release.artists[0].id
    artist_name = records.release.artists[0].name
    release_title = records.release.title
    artist_url = records.release.artists[0].url
    release_image_url = records.release.images[0]["uri"]
    genres = records.release.genres
    album_release_date = records.release.year
    main_release_date = records.release.master.fetch("year")
    folder = records.folder_id

    discogs_main_id = records.release.master.id
    #    print(dir(me.collection_folders[8].releases[0]))
    #    print(dir(me.collection_folders[8]))
    print(
        "Release ID: ", release_id,
        "Release URL: ", release_url,
        "Artist ID: ", artist_id,
        "Artist: ", artist_name,
        "Title: ", release_title,
        "Artist URL: ", artist_url,
        "Image URL: ", release_image_url,
        "Genre list: ", genres,
        "Album Release Date: ", album_release_date,
        "Main release date: ", main_release_date,
        "Main ID: ", discogs_main_id,
        "Folder ID: ", folder,
    )
