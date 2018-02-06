from datetime import datetime as dt
import pytz  # To make datetime objects 'aware'
from astral import Location
from satgeometry import get_complete_position


def is_night():
    """
    input: none
    output: boolean night or not
    """

    utc = pytz.UTC  # UTC Object

    lat, lon, city, region, time_zone = get_complete_position()
    current_location = Location((city, region, lat, lon, time_zone, 6))

    sunset = current_location.sun()['sunset']
    sunrise = current_location.sun()['sunrise']
    now = utc.localize(dt.now())

    return sunset < now and now < sunrise
