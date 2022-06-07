from sqlalchemy.future import select
from data import db_session
from data import config
import discogs_client

from data.album_data import Album
from data.genre_data import Genre
from data.main_release_data import Main_Data
from data.tracklist_data import Tracklists
import sqlalchemy
import json


me = config.my_data.identity()


async def get_album_db_data():

    for records in me.collection_folders[0].releases:
        album_data = Album()

        async with db_session.create_async_session() as session:
            release_id_query = select(Album.release_id).filter(Album.release_id == records.release.id)
            results = await session.execute(release_id_query)

            release_id_results = results.scalar_one_or_none()
            print("DB query results: ", release_id_results, "Type: ", type(release_id_results))

            if records.release.id == release_id_results:
                pass

            else:

                album_data.folder = records.folder_id
                album_data.release_id = records.release.id
                album_data.artist_id = records.release.artists[0].id
                album_data.artist_name = records.release.artists[0].name
                album_data.release_title = records.release.title

                album_data.release_url = records.release.url
                album_data.album_release_year = records.release.year

                try:
                    album_data.artist_url = records.release.artists[0].url

                except discogs_client.client.HTTPError:
                    album_data.artist_url = "None"

                try:
                    album_data.release_image_url = records.release.images[0]["uri"]

                except TypeError:
                    album_data.release_image_url = "None"

                async with db_session.create_async_session() as session:
                    session.add(album_data)
                    await session.commit()

        print(records, records.release.year)


async def update_db_data():
    pass


async def get_genre_data():
    # Need to match the int from each row and pass it to the method to get the main data
    for records in me.collection_folders[folder].releases:
        genre_data = Genre()

        async with db_session.create_async_session() as session:
            release_id_query = select(Genre.release_id).filter(Genre.release_id == records.release.id)
            results = await session.execute(release_id_query)

            release_id_results = results.scalar_one_or_none()

            if records.release.id == release_id_results:
                print("Record Release ID: ", records.release.id,
                      "SQL Query Results: ", release_id_results, "Already in db, pass")
                pass

            else:
                genre_data.release_id = records.release.id

                for genres in records.release.genres:
                    print("Genre: ", genres)
                    genre_data.release_id = records.release.id
                    genre_data.genres = genres

                    async with db_session.create_async_session() as session:
                        session.add(genre_data)
                        await session.commit()

            print("Adding to db: ", genre_data.release_id, genre_data.genres)


async def get_main_release_data():

    async with db_session.create_async_session() as session:
        release_id_query = select(Album.release_id)
        results = await session.execute(release_id_query)

        # Get all rows
        release_id_results = results.all()
        print(release_id_results[1], type(release_id_results[1]))

        # Need to match the int from each row and pass it to the method to get the main data
        for records in me.collection_folders[folder].releases:
            main_data = Main_Data()

            try:

                if records == me.collection_folders[folder].releases:
                    print(records.release.id, " Already in db, pass")
                    pass

                else:
                    main_data.release_id = records.release.id

                try:
                    main_data.main_release_date = records.release.master.fetch("year")
                    main_data.discogs_main_id = records.release.master.id
                    main_data.discogs_main_url = records.release.master.url

                except AttributeError:
                    #main_data.main_release_date = 1900
                    pass

                print("Adding to db", main_data.discogs_main_id)

                async with db_session.create_async_session() as session:
                    session.add(main_data)
                    await session.commit()

            except sqlalchemy.exc.IntegrityError:
                print("Already in db, pass")
                pass


async def get_tracklist_data():
    # Need to match the int from each row and pass it to the method to get the main data
    for records in me.collection_folders[folder].releases:
        tracklists = Tracklists()

        async with db_session.create_async_session() as session:
            release_id_query = select(Tracklists.release_id)\
                .filter(Tracklists.release_id == records.release.id)
            results = await session.execute(release_id_query)

            release_id_results = results.scalar_one_or_none()

            x = 0

            #if records.release.id == release_id_results:
            #    print("Record Release ID: ", records.release.id,
            #          "SQL Query Results: ", release_id_results, "Already in db, pass")
            #    pass

            # else:
            tracklists.release_id = records.release.id

            for tracks in records.release.tracklist:
                print("Tracks: ", tracks)
                tracklists.release_id = records.release.id
                tracklists.track_title = records.release.tracklist[x].title
                tracklists.track_duration = records.release.tracklist[x].duration
                tracklists.track_position = records.release.tracklist[x].position

                async with db_session.create_async_session() as session:
                    session.add(tracklists)
                    await session.commit()

                x = x + 1

            print("Adding to db: ", tracklists.release_id, tracklists.track_title)

