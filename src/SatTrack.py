#!/usr/bin/env python
from __future__ import print_function
import ephem
from datetime import datetime
from model import *
import json

# globals
try:
    with open('../config/config.json') as configuration_file:
        config = json.load(configuration_file)
except IOError:
    print('Config File not found, run configbuilder.py from the parent directory')
    sys.exit()
except ValueError as e:
    print('Invalid JSON: Error was: {}'.format(e))
    sys.exit()


def fetch_sat_tle(sat_name):
    pattern = '%{}%'.format(sat_name)
    db_satellite = Satellite.get(Satellite.name ** pattern)
    satellite = ephem.readtle(str(db_satellite.name).strip(),
                              str(db_satellite.lineone).strip(),
                              str(db_satellite.linetwo).strip())
    return satellite


def fetch_location(name):
    db_location = Location.get(Location.callsign == name)
    location = ephem.Observer()
    location.lat = db_location.lat * ephem.degree
    location.lon = db_location.lon * ephem.degree
    location.elevation = db_location.elevation
    return location


if __name__ == '__main__':
    """sample code to show how functions work
       Compare to http://www.amsat.org/amsat-new/tools/predict/index.php"""
    sat = fetch_sat_tle('SO-50')
    loc = fetch_location(config['default_location']['callsign'])
    sat.compute(loc)
    loc.date = datetime.utcnow()
    satpass = loc.next_pass(sat)
    print('Rise Time: {}, Azimuth:{}'.format(satpass[0], satpass[1]))
