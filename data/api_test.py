import config
import discogs_client
from discogs_client.models import Master

my_data = discogs_client.Client(config.agent, user_token=config.my_token)

chvrches_screen_violence = 20017387

print(my_data.release(chvrches_screen_violence).genres)

# print(discogs_data.identity().collection_foldes[8].releases[chvrches_screen_violence].release.id)
# print(discogs_data.release(20017387))
# print(my_data.release(20017387).url)
print(my_data.release(20017387).artists, my_data.release(20017387).title)
print(my_data.release(20017387).images[0]["uri"])
print(my_data.release(20017387).artists[0].name, type(my_data.release(1443762).artists))
print(my_data.release(20017387).artists[0].name)
print(my_data.release(2272402).year)
print(my_data.release(20017387).tracklist[0].title)
print(dir(my_data.release(20017387).tracklist[0]))
print(my_data.release(20017387).master.id)
# print(my_data.release(20017387).master.year)
# print(my_data.master(my_data.release(20017387).master.id).title)
print(dir(my_data.master))
# print(dir(my_data.release(20017387).value))

# main_release_date = my_data.master.items
# print(main_release_date)


# print(dir(my_data.master.release(2272402).year))

# d = config.discogs_data.identity() = User Object
# So this is me - only need it to call images and my collection data
# print(d.releases.releases(888785).release.id)

# Need to call the general / generic release API (but how)
# print(d.collection_folders[8].releases(888785).release.id)


# def get_genres():
#    for genre in d.release_genres():
#         print(genre)
