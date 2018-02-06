from datetime import datetime as dt  # for date and time
from sgp4.earth_gravity import wgs72  # for gravity correction
from sgp4.io import twoline2rv  # for reading TLE
import requests  # for requesting json from web
import json  # for parsing json files
import numpy as np
from scipy.interpolate import interp1d as inter

"""
print(satellite.error)    # nonzero on error

print(satellite.error_message)
"""

OBSERVER_ANGLE_ACCEPTABLE = 45
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

    if satellite.error != 0:
        return print("Satellite's position and velocity could not be found.")

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


def longlat_to_RA_DEC(latitude, longitude):
    """
    input: lat long angles
    output: RA and DEC
    """

    ra_map = inter([-180, 180], [0, 360])
    ra = ra_map(longitude)-180  # Needs to be mapped
    dec = latitude

    return ra, dec


def get_satellite_altitude(position):
    """
    input: satellites position (ASSUMING KM)
    output: altitude from earth center
    """

    return np.sqrt(position[0]**2+position[1]**2+position[2]**2)


def get_visible_area_radius(altitude):
    """
    input: altitude and OBSERVER_ANGLE_ACCEPTABLE
    output: radius of visible area
    """

    return np.tan(np.deg2rad(OBSERVER_ANGLE_ACCEPTABLE))*(altitude-EARTH_RADIUS_KM)


def get_visible_area_angle(altitude):
    """
    input: altitude of satellite
    output: angle of visible area from the center of the earth
    """

    visibleRadius = get_visible_area_radius(altitude)

    return np.rad2deg(np.arctan(visibleRadius/altitude))


def right_ascension(position):
    """
    input: position
    output: right ascension
    """

    return np.arctan(position[1]/position[0])


def declination(position):
    """
    input: position
    output: declination
    """

    return np.arctan(position[2]/np.hypot(position[0], position[1]))


def RA_DEC_from_position(position):
    """
    input: position
    output: right ascension and declination
    """

    return right_ascension(position), declination(position)


def angular_distance(position):
    """
    input: satellite position
    output: angular distance between GPS location and satellite
    """

    # Retreive RA and DEC for both objects
    ra_sat, dec_sat = RA_DEC_from_position(position)
    ra_obs, dec_obs = longlat_to_RA_DEC(get_position())

    # Converting from degrees to radians
    ra_sat, dec_sat, ra_obs, dec_obs = np.deg2rad([ra_sat, dec_sat, ra_obs, dec_obs])

    # Components to compute angular distance
    angle1 = np.sin(dec_obs)*np.sin(dec_sat)
    angle2 = np.cos(dec_obs)*np.cos(dec_sat)*np.cos(ra_obs-ra_sat)

    return np.arccos(angle1 + angle2)


def is_observable(angle, altitude):
    """
    input: angular distance between observer's position and satellite
    output: Boolean smaller/larger than OBSERVER_ANGLE_ACCEPTABLE
        True if in the range
    """

    visible_area_angle = get_visible_area_angle(altitude)

    return angle < visible_area_angle
