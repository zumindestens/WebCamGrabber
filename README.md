# WebCamScrap

Grab images from the Hurtigruten ships and save them with coordinates from Marinetraffic.
Creates a new folder for every new day.

Usage best in cronjobs.

example: python3 main.py "http://example.de" Lofoten /home/tea/
python3 main.py <source for image> <ship name> <basefolder> 

example for a cronjob:

`2,12,22,32,42,52 * * * * sudo -u www-data python3 /home/web-user/WebCamScrap/main.py https://hurtigruten.vossaskyen.no/en.no/hruten_mslofoten.jpg Lofoten /media/webcam 311950`
