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
    print("Today: ", today)
    search = str(today.month) + "-" + str(today.day)
    # search = '6-18'
    #search = '09-21'
    print("Search: ", search, type(search))

    async with db_session.create_async_session() as session:
        query = select(Album).filter(Album.mb_release_date.like('%' + search)).order_by(Album.mb_release_date)
        print(query)

        results = await session.execute(query)
        query_results = results.scalars()

        for data in query_results:
            print("Row: ", data)
            print("query_results: ", type(query_results))

            return query_results

        # for rows in query_results:
            # print("Row: ", rows, type(rows))

        #if str(query_results.mb_release_date[::-4]) == search:
        #    print("Search results: ", query_results)
        #else:
        #    print("No results")

