from starlette.requests import Request

import data.config as config
from data.choose import ChooseInfo
from data.config import my_data


class ChooseService:

    count = 0

    def get_choose_data():
        count = 0

        folder_data = []
        folder_id_data = []

        for folders in my_data.collection_folders:
            folder = my_data.collection_folders[count]
            folder_id = my_data.collection_folders.id[count]
            print(folder, folder.name)
            count += 1

            folder_data.append(folder)
            folder_id_data.append(folder_id)

            return folder_data, folder_id_data

        def get_album_data():
            release_data = config.my_data

            artist_count = 0

            for artist_name in release_data.release(album_release_id).artists:
                artist_name = (
                    release_data.release(album_release_id).artists[artist_count].name
                )

            artist_count += 1

            release_id = album_release_id

            artist_id = release_data.release(album_release_id).artists[0].name
            release_title = release_data.release(album_release_id).title
            genres = release_data.release(album_release_id).genres

        choose_info = ChooseInfo(
            folder,
            folder_number,
            release_id,
            release_title,
            artist_name,
            release_date,
            genres,
            main_release_date,
            album_release_date,
        )
        # print("Genres: ", genres)
        return album_info
