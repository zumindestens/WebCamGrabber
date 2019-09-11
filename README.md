# WebCamScrap

Grab images from the Hurtigruten ships and save them with coordinates from Marinetraffic.
Creates a new folder for every new day.

## Required Software

`apt install python3 python3-pip`

`pip3 install pytz ExifRead GPSPhoto pillow piexif`

## Cronjob Example

`2,12,22,32,42,52 * * * * sudo -u www-data python3 /home/web-user/WebCamScrap/main.py https://hurtigruten.vossaskyen.no/hruten_mslofoten.jpg Lofoten /media/webcam 311950`
