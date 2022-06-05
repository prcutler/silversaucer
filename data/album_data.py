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
    release_image_url: str = sa.Column(sa.String)
    album_release_date: str = sa.Column(sa.String)
    folder: int = sa.Column(sa.Integer)
