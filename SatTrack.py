#!/usr/bin/env python
from __future__ import print_function
import sqlite3
import ephem
import math
from datetime import datetime


# globals
degrees_per_radian = 180.0 / math.pi
db_name = 'sats.db'
conn = sqlite3.connect(db_name)

home = ephem.Observer()
home.lat = 43.612262
home.lon = -116.240718
home.elevation = 832


def fetch_sat_tle(sat_name):
    query = 'SELECT name, lineone, linetwo FROM satellites where name like \'%{}%\';'.format(sat_name)
    # print(query)
    cursor = conn.cursor()
    c = cursor.execute(query)
    first_match = c.fetchone()
    satellite = ephem.readtle(str(first_match[0]),
                              str(first_match[1]),
                              str(first_match[2]))
    return satellite


def fetch_location(name):
    query = 'SELECT name, lat, lon, elevation FROM locations where name = \'{}\';'.format(name)
    cursor = conn.cursor()
    c = cursor.execute(query)
    all_sats = c.fetchall()
    if len(all_sats) == 0:
        print('Location Not Found')
    elif len(all_sats) > 1:
        print('Multiple locations found, check username')
    else:
        location = ephem.Observer()
        location.lat = all_sats[0][1]
        location.lon = all_sats[0][2]
        location.elevation = all_sats[0][3]
    return location


sat = fetch_sat_tle('SO-50')
loc = fetch_location('matt')
sat.compute(loc)
loc.date = datetime.utcnow()
print('{}: altitude {} deg, azimuth {} deg'.format(sat.name, sat.alt * degrees_per_radian, sat.az * degrees_per_radian))
