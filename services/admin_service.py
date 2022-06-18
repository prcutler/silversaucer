from typing import List, Optional

from sqlalchemy.future import select
from data import db_session
from data import config
import discogs_client
import musicbrainzngs

from data.album_data import Album
from data.album import AlbumInfo
from data.genre_data import Genre
from data.main_release_data import Main_Data
from data.release import Release
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

                # async with db_session.create_async_session() as session:
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


async def update_mb_id():

    async with db_session.create_async_session() as session:

        query = select(Release.discogs_id, Release.m_rel_id).filter(Album.release_id == Release.discogs_id)
        results = await session.execute(query)
        release_id_results = results.fetchall()

        print("Count: ", len(release_id_results), release_id_results)
        # print("Tuple [7]", release_id_results[7])
        # results.all Returns a tuple: (124983, None), (190430, 'e5d96b48-c7dc-4a61-bf54-f32353fe08e5'),

        album_data = Album()

        for discogs_id, mb_id in release_id_results:

            if mb_id is not None:

                album_data.release_id = discogs_id
                album_data.mb_id = mb_id
                print("Release ID: ", album_data.release_id, "MusicBrainz ID: ", album_data.mb_id)

                #session.add(album_data)
                # Above line adds a blank row with only mb_id populated
                await session.commit()


# ## GET LIST OF ALL RELEASES MISSING MUSICBRAINZ RELEASE ID ###
async def missing_mb_info() -> List[Release]:
    async with db_session.create_async_session() as session:
        query = select(Album).filter(Album.mb_id == None).order_by(Album.artist_name.asc())

        results = await session.execute(query)
        releases = results.scalars()
        print(releases)

        return releases


async def view_edit(release_id: int):
    async with db_session.create_async_session() as session:
        query = select(Album).filter(Album.release_id == release_id)
        results = await session.execute(query)

        query_results = results.scalar_one_or_none()

        release_results = query_results
        print("Release results: ", release_results)

        # release_results.release_id = release_id
        release_url: Optional[str] = release_results.release_url
        artist_id: int = release_results.artist_id
        artist_name: Optional[str] = release_results.artist_name
        release_title: Optional[str] = release_results.release_title
        artist_url: Optional[str] = release_results.artist_url
        release_image_url: Optional[str] = release_results.release_image_url
        album_release_year: Optional[str] = release_results.album_release_year
        folder = release_results.folder
        mb_id: Optional[str] = release_results.mb_id
        mb_release_date = release_results.mb_release_date

        album_info = Album(
            release_url=release_url,
            release_id=release_id,
            artist_id=artist_id,
            artist_name=artist_name,
            release_title=release_title,
            artist_url=artist_url,
            release_image_url=release_image_url,
            album_release_year=album_release_year,
            folder=folder,
            mb_id=mb_id,
            mb_release_date=mb_release_date,
        )

        return album_info


async def edit_release(release_id: int, mb_id: str):
    async with db_session.create_async_session() as session:
        query = select(Album).filter(Album.release_id == release_id)
        results = await session.execute(query)

        query_results = results.scalar_one_or_none()

        release_results = query_results
        print("Release results: ", release_results)

        # release_results.release_id = release_id
        release_url: Optional[str] = release_results.release_url
        artist_id: int = release_results.artist_id
        artist_name: Optional[str] = release_results.artist_name
        release_title: Optional[str] = release_results.release_title
        artist_url: Optional[str] = release_results.artist_url
        release_image_url: Optional[str] = release_results.release_image_url
        album_release_year: Optional[str] = release_results.album_release_year
        folder = release_results.folder
        mb_id: Optional[str] = mb_id
        mb_release_date = release_results.mb_release_date
        print("Services Release ID: ", release_id, "MusicBrainz ID: ", mb_id)

        album_info = Album(
            release_url=release_url,
            release_id=release_id,
            artist_id=artist_id,
            artist_name=artist_name,
            release_title=release_title,
            artist_url=artist_url,
            release_image_url=release_image_url,
            album_release_year=album_release_year,
            folder=folder,
            mb_id=mb_id,
            mb_release_date=mb_release_date,
        )

        query_results.mb_id = mb_id

        await session.commit()

    return album_info


async def get_mb_date():
    async with db_session.create_async_session() as session:
        query = select(Album).filter(Album.mb_id is not None).filter(Album.mb_release_date == None)
        results = await session.execute(query)

        date_results = results.scalars()
        print(date_results)

        for musicbrainz in date_results:
            if musicbrainz.mb_id is not None:
                print(musicbrainz.mb_id)

                musicbrainzngs.set_useragent(
                    "silversaucer",
                    "0.1",
                    "https://github.com/prcutler/silversaucer/", )

                try:
                    musicbrainzngs.get_release_by_id(musicbrainz.mb_id)
                    mb_release_date = musicbrainzngs.get_release_by_id(musicbrainz.mb_id).get("release").get("date")
                except musicbrainzngs.musicbrainz.ResponseError:
                    mb_release_date = None

                musicbrainz.release_id = musicbrainz.release_id
                musicbrainz.mb_id = musicbrainz.mb_id
                musicbrainz.mb_release_date = mb_release_date
                print("Release ID: ", musicbrainz.release_id, "MusicBrainz ID: ", musicbrainz.mb_id, "Release Date: ", musicbrainz.mb_release_date)

                await session.commit()






