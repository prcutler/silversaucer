import asyncio
import traceback
from typing import List, Optional

from sqlalchemy import func, or_
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
from infrastructure.mb_ids import clean_date, normalize_artist, normalize_title
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


# Kinds of MusicBrainz entry an ID might belong to, in the order to try them.
_MB_ENTITY_LOOKUPS = [
    ("release", "get_release_by_id"),
    ("release-group", "get_release_group_by_id"),
    ("recording", "get_recording_by_id"),
    ("artist", "get_artist_by_id"),
    ("work", "get_work_by_id"),
    ("label", "get_label_by_id"),
]


def identify_mb_entity(mb_id: str):
    """Find out what a MusicBrainz ID refers to.

    Returns (kind, name, date), e.g. ("release-group", "EP3", "2014-03-24"),
    or (None, None, None) if MusicBrainz has nothing with that ID. Network
    and other non-404 errors are raised (musicbrainzngs.WebServiceError).
    """
    for kind, function_name in _MB_ENTITY_LOOKUPS:
        try:
            entity = getattr(musicbrainzngs, function_name)(mb_id)[kind]
        except musicbrainzngs.ResponseError as e:
            if getattr(e.cause, "code", None) == 404:
                continue
            raise
        name = entity.get("title") or entity.get("name")
        date = entity.get("date") or entity.get("first-release-date")
        return kind, name, date
    return None, None, None


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
            if release_id in seen and not (album.mb_id or "").strip()
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
            # Keep a date that was already entered (often by hand); only fill
            # it in when there isn't one.
            if not clean_date(album.mb_release_date):
                album.mb_release_date = mb_release_date
            summary["mb_matched"].append(album.release_id)
            print(
                "MusicBrainz match",
                album.release_id,
                mb_id,
                album.mb_release_date,
            )
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


# ---------------------------------------------------------------------------
# "Fix MusicBrainz data": search MusicBrainz for albums the Discogs link
# lookup couldn't match.
# ---------------------------------------------------------------------------


def _discogs_barcodes(release_id: int) -> List[str]:
    """Barcodes listed on the Discogs release, digits only."""
    try:
        identifiers = me.release(release_id).fetch("identifiers") or []
    except Exception as e:  # Discogs errors shouldn't stop the whole job
        print("Discogs lookup failed for", release_id, e)
        return []
    codes = []
    for identifier in identifiers:
        if identifier.get("type") != "Barcode":
            continue
        digits = "".join(c for c in identifier.get("value", "") if c.isdigit())
        if digits and digits not in codes:
            codes.append(digits)
    return codes


def _group_first_date(group_id: str) -> Optional[str]:
    group = musicbrainzngs.get_release_group_by_id(group_id)["release-group"]
    return group.get("first-release-date") or None


def _not_after_owned_copy(date: Optional[str], discogs_year) -> bool:
    """The original release can't be later than the edition you own."""
    try:
        owned_year = int(str(discogs_year).strip())
    except (TypeError, ValueError):
        return True
    if owned_year <= 0 or not date:
        return True
    return int(date[:4]) <= owned_year


def _search_by_barcode(album):
    """Exact barcode match. Returns (mb_id, date) or None.

    mb_id is only set when the barcode identifies a single release; if it
    matches several releases of one album, only the date is used.
    """
    for code in _discogs_barcodes(album["release_id"]):
        results = musicbrainzngs.search_releases(barcode=code, limit=10)
        releases = [r for r in results["release-list"] if r.get("barcode") == code]
        if not releases:
            continue

        groups = {r["release-group"]["id"] for r in releases}
        if len(groups) != 1:
            print(f"  barcode {code} matches {len(groups)} different albums, skipped")
            continue

        release = releases[0]
        same_artist = normalize_artist(release.get("artist-credit-phrase")) == normalize_artist(album["artist_name"])
        same_title = normalize_title(release.get("title")) == normalize_title(album["release_title"])
        if not (same_artist or same_title):
            print(f"  barcode {code} is \"{release.get('title')}\" by {release.get('artist-credit-phrase')}, skipped")
            continue

        date = _group_first_date(groups.pop())
        if not _not_after_owned_copy(date, album["album_release_year"]):
            print(f"  barcode {code}: date {date} is after your copy, skipped")
            continue

        mb_id = release["id"] if len(releases) == 1 else None
        return mb_id, date
    return None


def _search_by_title(album) -> Optional[str]:
    """Artist + title search for the album's original release date.

    Only accepts a single, unambiguous match: same artist, same title, and
    not dated after the copy you own. Returns the date or None.
    """
    artist = normalize_artist(album["artist_name"])
    title = normalize_title(album["release_title"])
    if not artist or not title:
        return None

    results = musicbrainzngs.search_release_groups(
        artist=artist, releasegroup=album["release_title"], limit=10
    )
    matches = [
        g
        for g in results["release-group-list"]
        if int(g.get("ext:score", 0)) >= 90
        and normalize_title(g.get("title")) == title
        and normalize_artist(g.get("artist-credit-phrase")) == artist
        and g.get("first-release-date")
    ]
    if len(matches) != 1:
        if len(matches) > 1:
            print(f"  {len(matches)} albums called \"{album['release_title']}\" by this artist, skipped")
        return None

    date = matches[0]["first-release-date"]
    if not _not_after_owned_copy(date, album["album_release_year"]):
        print(f"  title match dated {date} is after your copy, skipped")
        return None
    return date


def _search_musicbrainz(album) -> dict:
    """Blocking: try the barcode, then artist + title. Returns what was found:
    {"mb_id": ..., "date": ..., "method": ...}; values may be None."""
    found = {"mb_id": None, "date": None, "method": None}
    try:
        if not album["mb_id"]:
            barcode_match = _search_by_barcode(album)
            if barcode_match:
                found["mb_id"], found["date"] = barcode_match
                found["method"] = "barcode"

        if not found["date"] and not album["mb_release_date"]:
            date = _search_by_title(album)
            if date:
                found["date"] = date
                found["method"] = found["method"] or "artist + title"
    except musicbrainzngs.WebServiceError as e:
        print("MusicBrainz search failed for", album["release_id"], e)
    return found


async def fix_musicbrainz_data() -> dict:
    """Search MusicBrainz for every album missing an MB ID or release date.

    Fills in only what's missing: a barcode match can add the MB ID, and
    either search can add the original release date. Existing values are
    never changed. Every match is logged so it can be spot-checked.
    """
    summary = {"checked": 0, "id_added": [], "date_added": [], "not_found": 0}

    async with db_session.create_async_session() as session:
        query = (
            select(Album)
            .filter(
                or_(
                    Album.mb_id == None,
                    func.trim(Album.mb_id) == "",
                    Album.mb_release_date == None,
                    func.trim(Album.mb_release_date) == "",
                )
            )
            .order_by(Album.artist_name)
        )
        albums = (await session.execute(query)).scalars().all()
        print(f"Searching MusicBrainz for {len(albums)} albums")

        for n, album in enumerate(albums, 1):
            snapshot = {
                "release_id": album.release_id,
                "artist_name": album.artist_name,
                "release_title": album.release_title,
                "album_release_year": album.album_release_year,
                "mb_id": (album.mb_id or "").strip() or None,
                "mb_release_date": clean_date(album.mb_release_date),
            }
            found = await asyncio.to_thread(_search_musicbrainz, snapshot)
            summary["checked"] += 1

            changed = []
            if found["mb_id"] and not snapshot["mb_id"]:
                album.mb_id = found["mb_id"]
                summary["id_added"].append(album.release_id)
                changed.append(f"MB ID {found['mb_id']}")
            if found["date"] and not snapshot["mb_release_date"]:
                album.mb_release_date = found["date"]
                summary["date_added"].append(album.release_id)
                changed.append(f"date {found['date']}")

            label = f"{album.artist_name} - {album.release_title} ({album.release_id})"
            if changed:
                print(f"Matched by {found['method']}: {label}: {', '.join(changed)}")
                await session.commit()
            else:
                summary["not_found"] += 1
                print(f"No match: {label}")

            if n % 25 == 0:
                print(f"  ...{n}/{len(albums)} searched")

    print(
        f"MusicBrainz search complete: {summary['checked']} searched, "
        f"{len(summary['id_added'])} MB IDs added, "
        f"{len(summary['date_added'])} dates added, "
        f"{summary['not_found']} with no match"
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
            select(Album)
            .filter(or_(Album.mb_id == None, func.trim(Album.mb_id) == ""))
            .order_by(Album.artist_name.asc())
        )

        results = await session.execute(query)
        releases = results.scalars()
        print(releases)

        return releases


async def view_edit(release_id: int) -> Optional[Album]:
    """Return the album with this Discogs release ID, or None if there isn't one."""
    async with db_session.create_async_session() as session:
        query = select(Album).filter(Album.release_id == release_id)
        results = await session.execute(query)
        return results.scalars().first()


async def edit_release(
    release_id: int,
    *,
    artist_name: Optional[str],
    release_title: Optional[str],
    release_image_url: Optional[str],
    album_release_year: Optional[str],
    folder: Optional[int],
    mb_id: Optional[str],
    mb_release_date: Optional[str],
) -> Optional[Album]:
    """Save every editable field of an album. Values should already be
    validated and trimmed (see EditViewModel.validate). Returns the updated
    album, or None if there's no album with this release ID.

    The fields are keyword-only so callers can't pass them in the wrong order.
    """
    async with db_session.create_async_session() as session:
        query = select(Album).filter(Album.release_id == release_id)
        results = await session.execute(query)
        album = results.scalars().first()
        if album is None:
            return None

        album.artist_name = artist_name
        album.release_title = release_title
        album.release_image_url = release_image_url
        album.album_release_year = album_release_year
        album.folder = folder
        album.mb_id = mb_id
        album.mb_release_date = mb_release_date

        print("Saved edits to", release_id, "MusicBrainz ID:", mb_id)
        await session.commit()
        return album


async def get_mb_date():
    async with db_session.create_async_session() as session:
        query = (
            select(Album)
            .filter(Album.mb_id != None, func.trim(Album.mb_id) != "")
            .filter(
                or_(
                    Album.mb_release_date == None,
                    func.trim(Album.mb_release_date) == "",
                )
            )
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
