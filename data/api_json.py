import sqlalchemy as sa

from data.modelbase import SqlAlchemyBase


class JSONData(SqlAlchemyBase):
    __tablename__ = "json_data"

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    album: str = sa.Column(sa.String)
    artist: str = sa.Column(sa.String, index=True, unique=True)
    album_id: int = sa.Column(sa.Integer, index=True)
    image_url: str = sa.Column(sa.String)
