from typing import Any

from data.api_json import JSONData
from data.album_data import Album
from sqlalchemy.future import select
from data import db_session
from data import config

import requests

me = config.my_data.identity()

async def get_db_data() -> dict:

    album_data = Album()

    folder = 2162484
    x = 0

    for records in me.collection_folders[8].releases:
        release_id = records.release.id
        release_url = records.release.url
        artist_id = records.release.artists[0].id
        artist_name = records.release.artists[0].name
        release_title = records.release.title
        artist_url = records.release.artists[0].url
        release_image_url = records.release.images[0]["uri"]
        genres = records.release.genres
        release_date = records.release.year
        main_release_date = records.release.master.fetch("year")
        discogs_main_id = records.release.master.id

        async with db_session.create_async_session() as session:
            session.add(records)
            await session.commit()
 #       print(records)

async def update_db_data -> dict:
    pass
