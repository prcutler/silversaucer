from sqlalchemy.future import select
from data import db_session
from data.album_data import Album

import data.config as config
import pendulum


me = config.my_data


async def get_today_list():

    today = pendulum.today(tz="America/Chicago")
    print("Today: ", today, today.month, today.day)

    if today.month < 10 and today.day < 10:
        search = "0" + str(today.month) + "-0" + str(today.day)
    elif today.month < 10:
        search = "0" + str(today.month) + "-" + str(today.day)
    else:
        search = str(today.month) + "-" + str(today.day)

    # search = '06-19'
    # search = '09-21'
    print("Search: ", search, type(search))

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


async def get_month_list():

    today = pendulum.today(tz="America/Chicago")
    print("Today: ", today, today.month, today.day)

    if today.month < 10:
        search = "-" + "0" + str(today.month)
    else:
        search = str(today.month)

    print("Search: ", search, type(search))

    async with db_session.create_async_session() as session:
        query = (
            select(Album)
            .filter(Album.mb_release_date.like("%" + search + "%"))
            .order_by(Album.mb_release_date)
        )
        print(query)

        results = await session.execute(query)
        query_results = results.scalars()

        return query_results
