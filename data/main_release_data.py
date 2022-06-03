import datetime
from typing import List
import sqlalchemy as sa

from data.modelbase import SqlAlchemyBase


class Album(SqlAlchemyBase):
    __tablename__ = 'main_release_data'

    release_id: int = sa.Column(sa.Integer, index=True, primary_key=True)
    discogs_main_id: str = sa.Column(sa.String)
    discogs_main_url: str = sa.Column(sa.String)
    main_release_date: int = sa.Column(sa.String)