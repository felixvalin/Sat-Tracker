from datetime import datetime as dt
import pytz  # To make datetime objects 'aware'
from astral import Location
from satgeometry import get_position

ELEVATION_DEFAULT = 0


def is_night():
    """
    input: none
    output: boolean night or not
    """

    utc = pytz.UTC  # UTC Object

    lat, lon, city, region, time_zone = get_position(complete=True)
    current_location = Location((city, region, lat, lon, time_zone, ELEVATION_DEFAULT))

    sunset = current_location.sun()['sunset']
    sunrise = current_location.sun()['sunrise']
    now = utc.localize(dt.now())

    return sunset < now and now < sunrise
