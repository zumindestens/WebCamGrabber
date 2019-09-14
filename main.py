from datetime import datetime
import urllib.request
import os
import sys
import pytz
import requests
import traceback
from GPSPhoto import gpsphoto
import piexif
from PIL import Image

# example call: python3 main.py "http://example.de" Nordyl /home/tea/ marinetraffic id


class NoGPSInfoException(Exception):
    pass


def log(text, exception):
    assert isinstance(exception, Exception)
    with open(os.path.join(baseFolder, "log"), "a+") as file:
        file.write(datetime.now(timeZone).strftime("%Y-%m-%d_%H:%M:%S") + ": \n")
        file.write(text + "\n")
        file.write(traceback.format_exc())
        file.write("\n")


def createFolderIfPossible():
    folder = os.path.join(baseFolder, shipName + "-" + datetime.now(timeZone).strftime("%Y-%m-%d"))
    try:
        os.mkdir(folder)
    except FileExistsError:
        # expected behavior should only not reach this when there is a new day
        pass
    return folder


# setting gps coordinates of an existing image, copies it into the correct place, might raise NOGGSInfoException
def set_gps(filePath):
    # get GPS coordinates
    try:
        resp = requests.get("https://www.marinetraffic.com/map/getvesseljson/shipid:" + marineTrafficId,
                            headers=headers)
    except Exception as e:
        log("marinetraffic not reached",e)
        raise NoGPSInfoException
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

    folder = createFolderIfPossible()

    try:
        filePath = os.path.join(folder, shipName + datetime.now(timeZone).strftime(DATE_FORMAT_FILE) + ".jpg")
        brokenImg.save(filePath, exif=exif_bytes)
    except Exception as e:
        log("failed to save manipulated exif data", e)
        raise NoGPSInfoException


# initiallize values from call and time, open log
timeZone = pytz.timezone('CET')
url = sys.argv[1]
shipName = sys.argv[2]
baseFolder = sys.argv[3]
marineTrafficId = sys.argv[4]
DATE_FORMAT_FILE = "-%Y-%m-%d_%H-%M-%S"

# headers used for marinetraffic request
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

try:
    # get the latest image
    filePath = os.path.join(baseFolder, "current.jpg")
    urllib.request.urlretrieve(url, filePath)
except FileExistsError as f:
    log("Couldn't create new current.jpg file", f)
    sys.exit(2)
except Exception as e:
    log("Failed to receive webcam image", e)
    sys.exit(1)


try:
    set_gps(filePath)
except NoGPSInfoException:
    folder = createFolderIfPossible()
    newFilePath = os.path.join(folder, shipName + datetime.now(timeZone).strftime(DATE_FORMAT_FILE) + ".jpg")
    os.rename(filePath, newFilePath)
except Exception as e:
    log("Unknown Exception setting gps info", e)

try:
    os.remove(filePath)
except Exception as e:
    log("Couldn't delete file: current.jpg", e)

sys.exit(0)
