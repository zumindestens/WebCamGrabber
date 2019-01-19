import time
from datetime import datetime
import urllib.request
import os
import sys
import pytz
import requests
from GPSPhoto import gpsphoto
import piexif
from PIL import Image




# example call: python3 main.py "http://example.de" Nordyl /home/tea/

def new_folder():
    return baseFolder + shipName + "-" + datetime.now(timeZone).strftime("%d-%m-%Y")


timeZone = pytz.timezone('CET')
url = sys.argv[1]
shipName = sys.argv[2]
baseFolder = sys.argv[3]
marineTrafficId = sys.argv[4]
day = datetime.now(timeZone).day
folder = new_folder()

try:
    os.mkdir(folder)
except Exception:
    print("nothing todo as prob folder just already exists")

headers = {
"Host": "www.marinetraffic.com",
"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0",
"Accept": "application/json, text/plain, */*",
"Accept-Language": "de,en-US;q=0.7,en;q=0.3",
"Accept-Encoding": "gzip",
"Referer": "https://www.marinetraffic.com/en/ais/home/centerx:12.81882/centery:66.13328/zoom:8/mmsi:258477000/shipid:" + marineTrafficId,
"X-Requested-With": "XMLHttpRequest",
"DNT": "1",
"Connection": "keep-alive",
"Pragma": "no-cache",
"Cache-Control": "no-cache",
"TE": "Trailers"}


while True:
    if datetime.now(timeZone).day != day:
        day = datetime.now(timeZone).day
        folder = new_folder()
        os.mkdir(folder)

    time.sleep(5 * 60)

    try:
        filePath = folder + "/" + shipName + datetime.now(timeZone).strftime("-%H:%M") + ".jpg"
        urllib.request.urlretrieve(url, filePath)
    except Exception:
        # do nothing probably just a timeout
        print("")

    try:
        # get GPS coordinates
        resp = requests.get("https://www.marinetraffic.com/map/getvesseljson/shipid:" + marineTrafficId, headers=headers)
        longitude = resp.json()["LON"]
        latitude = resp.json()["LAT"]

        # set gps in exif
        photo = gpsphoto.GPSPhoto(filePath)
        info = gpsphoto.GPSInfo((float(latitude), float(longitude)))
        photo.modGPSData(info, filePath)

        # remove broken gps exif data
        brokenImg = Image.open(filePath)
        exif_dict = piexif.load(brokenImg.info["exif"])
        exif_dict["GPS"].pop(piexif.GPSIFD.GPSProcessingMethod, None)
        exif_bytes = piexif.dump(exif_dict)
        brokenImg.save(filePath, exif=exif_bytes)
    except Exception:
        # do nothing probably just a timeout
        print("")




