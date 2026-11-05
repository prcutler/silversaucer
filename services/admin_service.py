import asyncio
import traceback
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

me = config.my_data

musicbrainzngs.set_useragent(
    "silversaucer",
    "0.1",
    "https://github.com/prcutler/silversaucer/",
)


# Only one long-running import job at a time (per server process).
_job_running: Optional[str] = None


def job_in_progress() -> Optional[str]:
    """Name of the import job currently running, or None."""
    return _job_running


async def run_exclusive(name: str, job) -> None:
    """Run an async import job unless another one is already running.

    Meant to be scheduled as a background task so the web request returns
    immediately. Errors are logged rather than raised, since nobody is
    waiting on the result.
    """
    global _job_running
    if _job_running:
        print(f"Not starting {name}: {_job_running} is already running")
        return

    _job_running = name
    try:
        print(f"Starting {name}")
        await job()
        print(f"Finished {name}")
    except Exception:
        print(f"{name} failed:")
        traceback.print_exc()
    finally:
        _job_running = None


def _lookup_musicbrainz(discogs_release_id: int):
    """Find the MusicBrainz release linked to a Discogs release.

    Returns (mb_id, mb_release_date); either may be None. The date is the
    original release date of the album (see _original_release_date). MusicBrainz returns
    404 when no release links to this Discogs URL. musicbrainzngs enforces the
    1 request/second rate limit itself.
    """
    resource = f"https://www.discogs.com/release/{discogs_release_id}"
    try:
        result = musicbrainzngs.browse_urls(
            resource=resource, includes=["release-rels"]
        )
    except musicbrainzngs.ResponseError as e:
        if getattr(e.cause, "code", None) != 404:
            print("MusicBrainz lookup failed for", discogs_release_id, e)
        return None, None
    except musicbrainzngs.WebServiceError as e:
        print("MusicBrainz lookup failed for", discogs_release_id, e)
        return None, None

    relations = result.get("url", {}).get("release-relation-list", [])
    if not relations:
        return None, None
    if len(relations) > 1:
        print(
            "Multiple MusicBrainz releases for",
            discogs_release_id,
            [r["release"]["id"] for r in relations],
            "- using the first",
        )

    release = relations[0]["release"]
    mb_id = release["id"]
    return mb_id, _original_release_date(mb_id, fallback=release.get("date"))


def _original_release_date(mb_id: str, fallback: Optional[str] = None):
    """Return the original release date for a MusicBrainz release.

    This is the release group's first-release-date (the earliest date of any
    edition), so reissues get the album's original date rather than the
    reissue date. Falls back to `fallback` if MusicBrainz has no group date.
    """
    try:
        release = musicbrainzngs.get_release_by_id(
            mb_id, includes=["release-groups"]
        )["release"]
    except musicbrainzngs.WebServiceError as e:
        print("MusicBrainz release lookup failed for", mb_id, e)
        return fallback

    first_date = release.get("release-group", {}).get("first-release-date")
    return first_date or release.get("date") or fallback


def _build_album(record) -> Album:
    """Build an Album row from a Discogs collection item instance."""
    release = record.release
    album_data = Album()

    album_data.folder = record.folder_id
    album_data.release_id = release.id
    album_data.artist_id = release.artists[0].id
    album_data.artist_name = release.artists[0].name
    album_data.release_title = release.title
    album_data.release_url = release.url
    album_data.album_release_year = release.year

    try:
        album_data.artist_url = release.artists[0].url
    except discogs_client.client.HTTPError:
        album_data.artist_url = "None"

    try:
        album_data.release_image_url = release.images[0]["uri"]
    except (TypeError, IndexError):
        album_data.release_image_url = "None"

    return album_data


async def sync_collection() -> dict:
    """Incrementally sync every Discogs collection folder into the albums table.

    - Releases not yet in the database are added.
    - Releases already in the database whose folder changed in Discogs are moved.
    - Releases in the collection with no MusicBrainz ID are looked up on
      MusicBrainz (via the Discogs URL relationship) and get mb_id and
      mb_release_date filled in.
    - Releases in the database that are no longer in any folder are reported
      (not deleted), so nothing is lost by accident.

    Folder 0 ("All") is skipped because it duplicates every other folder.
    If the same release is in more than one folder, the first folder seen wins.
    """
    summary = {
        "added": [],
        "moved": [],
        "missing": [],
        "mb_matched": [],
        "mb_not_found": [],
        "folders": {},
    }

    async with db_session.create_async_session() as session:
        # Load what we already have once, instead of querying per record.
        results = await session.execute(select(Album))
        existing = {}
        for album in results.scalars():
            existing.setdefault(album.release_id, album)

        seen = set()

        # The Discogs and MusicBrainz clients make blocking HTTP calls, so run
        # them in a worker thread to keep the web server responsive.
        # config.my_data is a Client; folders belong to the User that the
        # token authenticates as.
        folders = await asyncio.to_thread(
            lambda: list(me.identity().collection_folders)
        )

        for folder in folders:
            if folder.id == 0:
                continue

            folder_added = 0
            print(f"Syncing folder {folder.name} ({folder.id}), {folder.count} items")

            records = await asyncio.to_thread(lambda: list(folder.releases))

            for record in records:
                release_id = record.release.id

                if release_id in seen:
                    # Another copy of a release we already handled this run.
                    continue
                seen.add(release_id)

                album = existing.get(release_id)

                if album is None:
                    album = await asyncio.to_thread(_build_album, record)
                    session.add(album)
                    existing[release_id] = album
                    summary["added"].append(release_id)
                    folder_added += 1
                    print("Adding to db", release_id, album.release_title)

                elif album.folder != record.folder_id:
                    print(
                        "Moving", release_id, "from", album.folder, "to", record.folder_id
                    )
                    album.folder = record.folder_id
                    summary["moved"].append(release_id)

            # Commit per folder so a failure part-way keeps earlier progress.
            await session.commit()
            summary["folders"][folder.name] = folder_added

        summary["missing"] = sorted(set(existing) - seen)

        # Fill in MusicBrainz data for anything in the collection that has no
        # MusicBrainz ID yet. Existing (possibly hand-picked) IDs are never
        # overwritten.
        need_mb = [
            album
            for release_id, album in existing.items()
            if release_id in seen and not album.mb_id
        ]
        print(f"Looking up {len(need_mb)} releases on MusicBrainz")

        for album in need_mb:
            mb_id, mb_release_date = await asyncio.to_thread(
                _lookup_musicbrainz, album.release_id
            )
            if mb_id is None:
                summary["mb_not_found"].append(album.release_id)
                continue

            album.mb_id = mb_id
            album.mb_release_date = mb_release_date
            summary["mb_matched"].append(album.release_id)
            print("MusicBrainz match", album.release_id, mb_id, mb_release_date)
            # Commit each match so a long run that fails keeps its progress.
            await session.commit()

    print(
        f"Sync complete: {len(summary['added'])} added, "
        f"{len(summary['moved'])} moved, "
        f"{len(summary['mb_matched'])} matched on MusicBrainz, "
        f"{len(summary['mb_not_found'])} not on MusicBrainz, "
        f"{len(summary['missing'])} in db but no longer in any Discogs folder"
    )

    return summary


async def get_album_db_data():
    return await sync_collection()


async def update_db_data():
    return await sync_collection()


async def get_main_release_data():
    async with db_session.create_async_session() as session:
        release_id_query = select(Album.release_id)
        results = await session.execute(release_id_query)

        folder=2162484

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
                    # main_data.main_release_date = 1900
                    pass

                print("Adding to db", main_data.discogs_main_id)

                #                async with db_session.create_async_session() as session:
                session.add(main_data)
                await session.commit()

            except sqlalchemy.exc.IntegrityError:
                print("Already in db, pass")
                pass


async def update_mb_id():
    async with db_session.create_async_session() as session:

        query = select(Release.discogs_id, Release.m_rel_id).filter(
            Album.release_id == Release.discogs_id
        )
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
                print(
                    "Release ID: ",
                    album_data.release_id,
                    "MusicBrainz ID: ",
                    album_data.mb_id,
                )

                # session.add(album_data)
                # Above line adds a blank row with only mb_id populated
                await session.commit()


# ## GET LIST OF ALL RELEASES MISSING MUSICBRAINZ RELEASE ID ###
async def missing_mb_info() -> List[Release]:
    async with db_session.create_async_session() as session:
        query = (
            select(Album).filter(Album.mb_id == None).order_by(Album.artist_name.asc())
        )

        results = await session.execute(query)
        releases = results.scalars()
        print(releases)

        return releases


async def view_edit(release_id: int):
    async with db_session.create_async_session() as session:
        query = select(Album).filter(Album.release_id == release_id)
        results = await session.execute(query)

        query_results = results.scalar()

        release_results = query_results
        print("Release results: ", release_results)

        # release_results.release_id = release_id

        try:
            release_url: Optional[str] = release_results.release_url

        except AttributeError:
            release_url = None

        artist_id: int = release_results.artist_id
        artist_name: Optional[str] = release_results.artist_name
        release_title: Optional[str] = release_results.release_title
        artist_url: Optional[str] = release_results.artist_url

        try:
            release_image_url: Optional[str] = release_results.release_image_url

        except AttributeError:
            release_image_url = None

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


async def edit_release(
    release_id: int,
    release_title: str,
    artist_name: str,
    release_image_url: str,
    album_release_year: str,
    folder: int,
    mb_id: str,
    mb_release_date: str,
):
    async with db_session.create_async_session() as session:
        query = select(Album).filter(Album.release_id == release_id)
        results = await session.execute(query)

        query_results = results.scalar_one_or_none()

        release_results = query_results
        print("Release results: ", release_results)

        # release_results.release_id = release_id
        release_url: Optional[str] = release_results.release_url
        artist_id: int = release_results.artist_id
        artist_name: Optional[str] = artist_name
        release_title: Optional[str] = release_title
        artist_url: Optional[str] = release_results.artist_url
        release_image_url: Optional[str] = release_image_url
        album_release_year: Optional[str] = album_release_year
        folder = folder
        mb_id: Optional[str] = mb_id
        mb_release_date = mb_release_date
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

        query_results.album_release_year = album_release_year
        query_results.mb_id = mb_id
        query_results.mb_release_date = mb_release_date

        await session.commit()

    return album_info


async def get_mb_date():
    async with db_session.create_async_session() as session:
        query = (
            select(Album)
            .filter(Album.mb_id != None)
            .filter(Album.mb_release_date == None)
        )
        results = await session.execute(query)

        date_results = results.scalars()
        print(date_results)

        for musicbrainz in date_results:
            if musicbrainz.mb_id is not None:
                print(musicbrainz.mb_id)

                mb_release_date = await asyncio.to_thread(
                    _original_release_date, musicbrainz.mb_id
                )

                musicbrainz.release_id = musicbrainz.release_id
                musicbrainz.mb_id = musicbrainz.mb_id
                musicbrainz.mb_release_date = mb_release_date
                print(
                    "Release ID: ",
                    musicbrainz.release_id,
                    "MusicBrainz ID: ",
                    musicbrainz.mb_id,
                    "Release Date: ",
                    musicbrainz.mb_release_date,
                )

                await session.commit()


async def get_new_release_data(release_id: int):

    release_id = release_id
    release_url = me.release(release_id).url
    artist_id = me.release(release_id).artists[0].id
    artist_name = me.release(release_id).artists[0].name
    release_title = me.release(release_id).title
    artist_url = me.release(release_id).artists[0].url
    release_image_url = me.release(release_id).images[0]["uri"]
    album_release_year = me.release(release_id).year

    album_info = AlbumInfo(
        release_id,
        release_url,
        artist_id,
        artist_name,
        release_title,
        artist_url,
        release_image_url,
        genres=None,
        main_release_date=None,
        album_release_year=album_release_year,
        track_title=None,
        track_duration=None,
        track_position=None,
        track_info=None,
        mb_id=None,
        mb_release_date=None,
    )
    print("Album Info: ", album_info)

    return album_info


async def add_new_release(release_id):
    async with db_session.create_async_session() as session:
        query = select(Album).filter(Album.release_id == release_id)
        results = await session.execute(query)

        query_results = results.scalar_one_or_none()

        release_results = query_results
        print("Release results: ", release_results)

        if release_results is None:
            print("Release ID: ", release_id)

            release_url = me.release(release_id).url
            artist_id = me.release(release_id).artists[0].id
            artist_name = me.release(release_id).artists[0].name
            release_title = me.release(release_id).title
            artist_url = me.release(release_id).artists[0].url
            release_image_url = me.release(release_id).images[0]["uri"]
            album_release_year = me.release(release_id).year

            album_info = Album(
                release_url=release_url,
                release_id=release_id,
                artist_id=artist_id,
                artist_name=artist_name,
                release_title=release_title,
                artist_url=artist_url,
                release_image_url=release_image_url,
                album_release_year=album_release_year,
                folder=2162484,
                mb_id=None,
                mb_release_date=None,
            )

            session.add(album_info)
            await session.commit()

            return album_info

        else:
            return None
