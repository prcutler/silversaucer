from starlette.requests import Request
from typing import List, Optional
from sqlalchemy.future import select
from data import db_session
from data.album_data import Album
from data.today_data import TodayInfo

import data.config as config
import pendulum
import sqlalchemy


me = config.my_data


async def get_today_list():

    today = pendulum.today()
    print("Today: ", today, today.month, today.day)

    if today.month < 10:
        search = "0" + str(today.month) + "-" + str(today.day)
    else:
        search = str(today.month) + "-" + str(today.day)

    # search = '06-21'
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

        for data in query_results:
            print("Row: ", data)
            print("query_results: ", type(query_results))

            return query_results


