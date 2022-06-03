import datetime
from typing import List
import sqlalchemy as sa

from data.modelbase import SqlAlchemyBase


class Album(SqlAlchemyBase):
    __tablename__ = 'genres'

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    release_id: int = sa.Column(sa.Integer, index=True)
    genres: str = sa.Column(sa.String)
