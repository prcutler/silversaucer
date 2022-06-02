from typing import Any

from data.album_data import Album
from sqlalchemy.future import select
from data import db_session
from data import config
import discogs_client

import requests

me = config.my_data.identity()


async def get_db_data():

    folder = 2162484
    x = 0

    for records in me.collection_folders[8].releases:
        album_data = Album()

        try:

            album_data.release_id = records.release.id
            album_data.release_url = records.release.url
            album_data.artist_id = records.release.artists[0].id
            album_data.artist_id = None
            album_data. artist_name = records.release.artists[0].name
            album_data.release_title = records.release.title
            album_data.artist_url = records.release.artists[0].url
            album_data.release_image_url = records.release.images[0]["uri"]
            #album_data.genres = records.release.genres
            album_data.release_date = records.release.year
            album_data.main_release_date = records.release.master.fetch("year")
            album_data.discogs_main_id = records.release.master.id
            album_data.folder = folder

        except discogs_client.client.HTTPError:
            pass

        print(records)

        async with db_session.create_async_session() as session:
            session.add(album_data)
            await session.commit()




async def update_db_data():
    pass
