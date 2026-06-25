from sqlalchemy import func
from sqlalchemy.future import select
from data import db_session
from data.album_data import Album

import data.config as config
import pendulum


me = config.my_data


async def get_today_list(offset: int = 0):

    target_date = pendulum.today(tz="America/Chicago").add(days=offset)
    search = target_date.format("MM-DD")
    print("Target date: ", target_date, "Search: ", search)

    async with db_session.create_async_session() as session:
        query = (
            select(Album)
            .filter(Album.mb_release_date.like("%" + search))
            .order_by(Album.mb_release_date)
        )
        print(query)

        results = await session.execute(query)
        query_results = results.scalars()

        return query_results


async def get_month_list(offset: int = 0):

    target_date = pendulum.today(tz="America/Chicago").add(months=offset)
    search = "{:02d}".format(target_date.month)
    print("Target month: ", target_date, "Search month: ", search)

    async with db_session.create_async_session() as session:
        trimmed_date = func.trim(Album.mb_release_date)
        query = (
            select(Album)
            .filter(func.substr(trimmed_date, 6, 2) == search)
            .order_by(func.substr(trimmed_date, 9, 2))
        )
        print(query)

        results = await session.execute(query)
        query_results = results.scalars()

        return query_results
