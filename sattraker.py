from datetime import datetime as dt  # for date and time
from sgp4.earth_gravity import wgs72  # for gravity correction
from sgp4.io import twoline2rv  # for reading TLE
import requests  # for requesting json from web
import json  # for parsing json files
import numpy as np

"""
print(satellite.error)    # nonzero on error

print(satellite.error_message)
"""
VIEWER_ANGLE_ACCEPTABLE = 45
LATITUDE_DEFAULT = 45
LONGITUDE_DEFAULT = -75
EARTH_RADIUS_KM = 6370


def get_fromfile_TLE(filename):
    """
    input: file with TLE orbit parameters
    output: 2 lines for processing
    """

    f = open(filename, 'r')
    line1 = f.read()
    line2 = f.read()
    f.close()

    return line1, line2


def get_sat_posvel_curr(TLE):
    """
    input: TLE parameters
    output: positions and velocities for satellite at current UTC time
    """

    line1, line2 = TLE
    satellite = twoline2rv(line1, line2, wgs72)
    currTime = dt.utcnow()
    position, velocity = satellite.propagate(currTime.year, currTime.month, currTime.day, currTime.hour, currTime.minute, currTime.second)

    return position, velocity


def get_position():
    """
    input: none
    output: latitude, longitude
    """

    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']

    return lat, lon


def get_satellite_altitude(position):
    """
    input: satellites position (ASSUMING KM)
    output: altitude from ground
    """

    return np.sqrt(position[0]**2+position[1]**2+position[2]**2)-EARTH_RADIUS_KM
