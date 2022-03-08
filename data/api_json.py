
import sqlalchemy as sa

from data.modelbase import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'api_json'

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    album: str = sa.Column(sa.String)
    artist: str = sa.Column(sa.String, index=True, unique=True)
    album_id: in = sa.Column(sa.Integer, index=True)
    image_url: str = sa.Column(sa.String)