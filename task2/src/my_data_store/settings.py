import os


class Settings:
    FORMAT = os.environ.get('FORMAT', 'json')
    DESTINATION = os.environ.get('DESTINATION', 'local')
