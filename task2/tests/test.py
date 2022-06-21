# Import Module
import ftplib

# Fill Required Information
HOSTNAME = "192.168.1.100"
USERNAME = "demo"
PASSWORD = "demo"
# Connect FTP Server
ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)

# force UTF-8 encoding
ftp_server.encoding = "utf-8"

# Enter File Name with Extension
filename = "file.json"

# Read file in binary mode
with open(filename, "rb") as file:
    # Command for Uploading the file "STOR filename"
    ftp_server.storbinary(f"STOR {filename}", file)

print(ftp_server.dir())
