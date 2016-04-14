#!/usr/bin/env python
from __future__ import print_function
import sqlite3
import ephem
import math
from datetime import datetime
import sys
import json

# globals
try:
    with open('../config/config.json') as configuration_file:
        config = json.load(configuration_file)
except IOError:
    print('Config File not found')
    sys.exit()
except ValueError as e:
    print('Invalid JSON: Error was: {}'.format(e))
    sys.exit()

degrees_per_radian = 180.0 / math.pi
db_name = config['datasource']['filename']


def fetch_sat_tle(sat_name):
    query = 'SELECT name, lineone, linetwo FROM satellites where name like ?;'
    params = (sat_name,)
    # print(query)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    c = cursor.execute(query, params)
    first_match = c.fetchone()
    satellite = ephem.readtle(str(first_match[0]),
                              str(first_match[1]),
                              str(first_match[2]))
    conn.close()
    return satellite


def fetch_location(name):
    query = 'SELECT callsign, lat, lon, elevation, timezone FROM locations where callsign = ?;'
    params = (name,)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    c = cursor.execute(query, params)
    all_locs = c.fetchall()
    if len(all_locs) == 0:
        print('Location Not Found')
        conn.close()
        sys.exit()
    elif len(all_locs) > 1:
        print('Multiple locations found, check username')
        conn.close()
        sys.exit()
    else:
        # print(all_locs)
        location = ephem.Observer()
        location.lat = all_locs[0][1] * ephem.degree
        location.lon = all_locs[0][2] * ephem.degree
        location.elevation = all_locs[0][3]
    conn.close()
    return location


if __name__ == '__main__':
    """sample code to show how functions work
       Compare to http://www.amsat.org/amsat-new/tools/predict/index.php"""
    sat = fetch_sat_tle('SO-50')
    loc = fetch_location('W1AW')
    sat.compute(loc)
    loc.date = datetime.utcnow()
    satpass = loc.next_pass(sat)
    print('Rise Time: {}, Azimuth:{}'.format(satpass[0], satpass[1]))
