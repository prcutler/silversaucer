from typing import Any

from data.album_data import Album
from sqlalchemy.future import select
from data import db_session
from data import config
import discogs_client

from data.album_data import Album
from data.genre_data import Genre
from data.main_release_data import Main_Data
from data.tracklist_data import Tracklists


me = config.my_data.identity()
folder = 8
folder_id = 2162484


async def get_album_db_data():

    for records in me.collection_folders[folder].releases:
        album_data = Album()

        async with db_session.create_async_session() as session:
            release_id_query = select(Album.release_id).filter(Album.release_id == records.release.id)
            results = await session.execute(release_id_query)

            release_id_results = results.scalar_one_or_none()
            print("DB query results: ", release_id_results, "Type: ", type(release_id_results))

            if records.release.id == release_id_results:
                pass

            else:

                try:

                    album_data.folder = folder_id
                    album_data.release_id = records.release.id
                    album_data.release_url = records.release.url
                    album_data.artist_id = records.release.artists[0].id
                    album_data.artist_name = records.release.artists[0].name
                    album_data.release_title = records.release.title
                    album_data.artist_url = records.release.artists[0].url

                    album_data.genres = records.release.genres[0]
                    album_data.album_release_date = records.release.year

                    if records.release.images[0]["uri"] is not None:
                        album_data.release_image_url = records.release.images[0]["uri"]
                    else:
                        continue

                    async with db_session.create_async_session() as session:
                        session.add(album_data)
                        await session.commit()

                except discogs_client.client.HTTPError:
                    pass

        print(records, records.release.year)


async def update_db_data():
    pass


async def get_genre_data():
    pass


async def get_main_release_data():

    async with db_session.create_async_session() as session:
        release_id_query = select(Album.release_id).filter(Album.release_id)
        results = await session.execute(release_id_query)

        release_id_results = results.scalar()

        for records in release_id_results:
            main_data = Main_Data()

            if records.release.master is not None:
                main_data.main_release_date = records.release.master.fetch("year")
                main_data.discogs_main_id = records.release.master.id
                main_data.discogs_main_url = records.release.master.url

                async with db_session.create_async_session() as session:
                    session.add(main_data)
                    await session.commit()

            else:
                continue


async def get_tracklist_data():
    pass

