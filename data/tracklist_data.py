import datetime
from typing import List
import sqlalchemy as sa

from data.modelbase import SqlAlchemyBase


class Album(SqlAlchemyBase):
    __tablename__ = 'tracks'

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    release_id: int = sa.Column(sa.Integer, index=True)
    track_position: str = sa.Column(sa.String)
    track_title: str = sa.Column(sa.String)
    track_duration: str = sa.Column(sa.String)
