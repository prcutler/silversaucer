import datetime
from typing import List
import sqlalchemy as sa

from data.modelbase import SqlAlchemyBase


class Album(SqlAlchemyBase):
    __tablename__ = 'albums'

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    release_id: int = sa.Column(sa.Integer, index=True)
    release_url: str = sa.Column(sa.String)
    artist_id: int = sa.Column(sa.Integer, index=True)
    artist_name: str = sa.Column(sa.String)
    release_title: str = sa.Column(sa.String)
    artist_url: str = sa.Column(sa.String)
    release_image_url: str = sa.Column(sa.String, index=True)
    genres: List[str] = sa.Column(sa.String, index=True)
    discogs_main_id: str = sa.Column(sa.String, index=True)
    discogs_main_url: str = sa.Column(sa.String)
    main_release_date: int = sa.Column(sa.Integer)
    album_release_date: str = sa.Column(sa.String)
    track_title: List[str] = sa.Column(sa.String)
    track_duration: List[str] = sa.Column(sa.String)
    track_position: List[str] = sa.Column(sa.String)
