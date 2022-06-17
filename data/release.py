import datetime
from typing import List
import sqlalchemy as sa

from data.modelbase import SqlAlchemyBase


class Release(SqlAlchemyBase):
    __tablename__ = 'release'

    discogs_id: int = sa.Column(sa.Integer, primary_key=True)

    discogs_title: int = sa.Column(sa.String)
    import_timestamp: str = sa.Column(sa.String)
    d_artist: str = sa.Column(sa.String)
    in_d_collection:int = sa.Column(sa.Integer)
    m_rel_id: str = sa.Column(sa.String)
    m_rel_id_override: str = sa.Column(sa.String)
    m_match_time: str = sa.Column(sa.String)
    d_catno: str = sa.Column(sa.String)
    m_match_method: str = sa.Column(sa.String)
