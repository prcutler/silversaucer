import config
import discogs_client

d = discogs_client.Client(config.agent, user_token=config.my_token)

chvrches_screen_violence = 20017387

print(dir(d.release(20017387)))

print(d.release(20017387).genres)

print("Title: ", d.release(20017387).title)

# print(discogs_data.identity().collection_folders[8].releases[chvrches_screen_violence].release.id)
# print(discogs_data.release(20017387))
# print(d.release(20017387).url)
print(d.release(11589538).artists, d.release(11589538).title)
print(d.release(20017387).images[0]["uri"])
print(d.release(20017387).artists[0].name, type(d.release(1443762).artists))
print(d.release(20017387).artists[0].name)
print(d.release(2272402).year)
print(d.release(20017387).tracklist[0].title)
print(dir(d.release(20017387).tracklist[0]))
print(d.release(20017387).master.id)
# print(d.release(20017387).master.year)
# print(d.master(d.release(20017387).master.id).title)
print(dir(d.master))
print(d.release(20017387).images[0])
# print(dir(d.release(20017387).value))

print(d.release(20017387).master.fetch("year"))
print(d.release(20017387).artists[0].url)

# main_release_date = d.master.items
# print(main_release_date)


# print(dir(d.master.release(2272402).year))

# d = config.discogs_data.identity() = User Object
# So this is me - only need it to call images and my collection data
# print(d.releases.releases(888785).release.id)

# Need to call the general / generic release API (but how)
# print(d.collection_folders[8].releases(888785).release.id)


# def get_genres():
#    for genre in d.release_genres():

#         print(genre)
#       print(genre)
