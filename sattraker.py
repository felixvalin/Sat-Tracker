from datetime import datetime as dt  # for date and time
from sgp4.earth_gravity import wgs72  # for gravity correction
from sgp4.io import twoline2rv  # for reading TLE
import requests  # for requesting json from web
import json  # for parsing json files

"""
line1 = ('1 00005U 58002B   00179.78495062  .00000023  00000-0  28098-4 0  4753')
line2 = ('2 00005  34.2682 348.7242 1859667 331.7664  19.3264 10.82419157413667')
satellite = twoline2rv(line1, line2, wgs72)
position, velocity = satellite.propagate(2000, 6, 29, 12, 50, 19)

print(satellite.error)    # nonzero on error

print(satellite.error_message)

print(position)

print(velocity)
"""


def get_TLE(filename):
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
