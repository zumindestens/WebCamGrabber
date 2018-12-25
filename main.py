import time
from datetime import datetime
import urllib.request
import os
import sys
import pytz


# example call: python3 main.py "http://example.de" Nordyl /home/tea/

def new_folder():
    return baseFolder + shipName + "-" + datetime.now(timeZone).strftime("%d-%m-%Y")


timeZone = pytz.timezone('CET')
url = sys.argv[1]
shipName = sys.argv[2]
baseFolder = sys.argv[3]
day = datetime.now(timeZone).day
folder = new_folder()

try:
    os.mkdir(folder)
except Exception:
    print("nothing todo as prob folder just already exists")


while True:
    if datetime.now(timeZone).day != day:
        day = datetime.now(timeZone).day
        folder = new_folder()
        os.mkdir(folder)

    time.sleep(5 * 60)
    filePath = folder + "/" + shipName + datetime.now(timeZone).strftime("-%H:%M") + ".jpg"
    urllib.request.urlretrieve(url, filePath)
