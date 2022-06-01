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

print(me.collection_folders)

#for item in me.collection_folders[8].releases:
#    print(item)

for records in me.collection_folders[8].releases:
    release_id = records.release.id
    release_url = records.release.url
    artist_id = records.release.artists[0].id
    artist_name = records.release.artists[0].name
    release_title = records.release.title
    artist_url = records.release.artists[0].url
    release_image_url = records.release.images[0]
    genres = records.release.genres
    album_release_date = records.release.year
    main_release_date = records.release.master.fetch("year")
    if main_release_date == 0:
        main_release_date = release_date
    else:
        main_release_date = main_release_date
    discogs_main_id = records.release.master.id
#    print(dir(me.collection_folders[8].releases[0]))
#    print(dir(me.collection_folders[8]))
    print(release_id, release_url, artist_id, artist_name, release_title, artist_url, release_image_url, genres, album_release_date, main_release_date, discogs_main_id)