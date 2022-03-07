from typing import List
import sqlalchemy as sa
from data.modelbase import SqlAlchemyBase


class AlbumInfo(SqlAlchemyBase):

    __tablename__ = 'album_info'

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    release_id: int = sa.Column(sa.Integer)
    release_url: str = sa.Column(sa.String, index=True)
    artist_id: int = sa.Column(sa.Integer, index=True)
    artist_name: str = sa.Column(sa.String)
    release_title: str = sa.Column(sa.String)
    artist_url: str = sa.Column(sa.String)
    release_image_url: str = sa.Column(sa.String)
    genres: List[str] = sa.Column(sa.String)
    # discogs_main_id: str,
    # discogs_main_url: str,
    main_release_date: int = sa.Column(sa.Integer)
    album_release_date: str = sa.Column(sa.String)
    track_title: str = sa.Column(sa.String)
    track_duration: str = sa.Column(sa.String)
    track_position: str = sa.Column(sa.String)

