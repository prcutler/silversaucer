import datetime


class User:
    def __init__(self, username, password):
        self.id = 1
        self.username = username
        self.password = password
        self.last_login: datetime.datetime = None
