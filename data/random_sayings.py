import random

random_sayings = [
    "Listen to this, meatbag:",
    "Put these tunes on:",
    "Head bang to this album:",
    "Turn the volume up to 11 and play this:",
    "Air guitar to this album:",
    "Don't play the air drums while you listen to this:",
    "This is the best album ever:",
    "Is this the worst album ever?",
    "Don't you dare hit refresh. Listen to this first: ",
    "I don't care what you like, but I like this:",
    "Crank it up while you listen to this:",
    "Drop the needle on this:",
]


def get_random_saying():
    random_saying = random.choice(random_sayings)
    return random_saying
