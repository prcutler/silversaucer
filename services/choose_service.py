from starlette.requests import Request

import data.config as config
from data.choose import ChooseInfo
from data.config import my_data


class ChooseService:

    count = 0

    def get_choose_data():
        count = 0

        for folders in my_data.collection_folders:
            folder = my_data.collection_folders[count]

            count += 1

            return folder

        def get_album_data():
            release_data = config.my_data

            artist_count = 0

            for data in release_data.collection_folders[1]:
                artist_name = release_data.releasename

                artist_id = artist_name
                release_id = album_release_id
                release_title = release_data.release(album_release_id).title
                genres = release_data.release(album_release_id).genres
                album_release_date = release_data.release(album_release_id).year

            choose_info = ChooseInfo(
                release_id,
                artist_id,
                release_title,
                genres,
                album_release_date,
            )
            # print("Genres: ", genres)
            return album_info
