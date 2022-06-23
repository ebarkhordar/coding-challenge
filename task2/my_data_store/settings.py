import os


class Settings:
    SUPPORTED_FORMATS = ['json', 'xml', 'binary']
    SUPPORTED_DESTINATIONS = ['local drive', 'ftp']
    FTP_HOSTNAME = os.environ.get('FTP_HOSTNAME', '192.168.1.100')
    FTP_USERNAME = os.environ.get('FTP_USERNAME', 'demo')
    FTP_PASSWORD = os.environ.get('FTP_PASSWORD', 'demo')
