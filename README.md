# SatTrack
Under documented and tested idea where a user can find out if an amateur radio satellite pass is going to occur when the user (location) is available.

There are 3 main data objects.
1. Satellite Info (tlehandler.py)- This is stored in two line element format.  The information is retrieved from amsat or celestrak.
2. Location (UserManager.py) - This is geo information about a user using a unique identifier (usually callsign).  Lat/Lon information comes from callook.info, elevation is pulled from google's geocode API.
3. Timeslot (TimeSlotHandler.py) - Timeslots are the times a location is available to catch a satellite pass.

SatTrack.py puts all of the information together and uses PyEphem to calculate the next pass from a given time, lat, lon, and elevation.  This will then spit out a list of potential good passes when the location is available to work the sat.


