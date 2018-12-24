import time
import datetime
import urllib.request
import os
import sys


def new_folder():
    return baseFolder + shipName + "-" + datetime.datetime.now().strftime("%d-%m-%Y")


url = sys.argv[1]
shipName = sys.argv[2]
baseFolder = sys.argv[3]
day = datetime.datetime.now().day
folder = new_folder()

try:
    os.mkdir(folder)
except Exception:
    print("nothing todo as prob folder just already exists")


while True:
    if datetime.datetime.now().day != day:
        day = datetime.datetime.now().day
        folder = new_folder()
        os.mkdir(folder)

    time.sleep(1 * 60)
    urllib.request.urlretrieve(url, folder + "/" + shipName + datetime.datetime.now().strftime("-%H:%M") + ".jpg")
