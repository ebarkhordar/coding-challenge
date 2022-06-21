import os


class Settings:
    FORMAT = os.environ.get('FORMAT', 'json')
    DESTINATION = os.environ.get('DESTINATION', 'local drive')
    FTP_HOSTNAME = "192.168.1.100"
    FTP_USERNAME = "demo"
    FTP_PASSWORD = "demo"
