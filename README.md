# SatTrack
Under documented and tested idea where a user can find out if an amateur radio satellite pass is going to occur when the user (location) is available.

There are 3 main data objects.

1. Satellite Info (tlehandler.py)- This is stored in two line element format.  The information is retrieved from amsat or celestrak.

2. Location (UserManager.py) - This is geo information about a user using a unique identifier (usually callsign).  Lat/Lon information comes from callook.info, elevation is pulled from google's geocode API.


3. Timeslot (TimeSlotHandler.py) - Timeslots are the times a location is available to catch a satellite pass.


SatTrack.py puts all of the information together and uses PyEphem to calculate the next pass from a given time, lat, lon, and elevation.  This will then spit out a list of potential good passes when the location is available to work the sat.


There's a long todo list including formatting, correecting timezones in places.  Ultimately this will be wrapped into a REST API.

To use as it currently exists:

1. Create a new sqlite3 database.
2. Install required libraries (see requirements.txt).
3. Apply the schema.sql to the newly created DB.
4. Copy sampleconfig.json to config.json.
5. Update config.json to point at the newly created sqlite3 database.
6. Change the callsign in __main__ of UserManager.py to your own.
7. Edit the __main__ section of TimeSlotHandler for your availability.
8. Run python tlehandler.py - This will seed the satellite database with the latest info from amsat.
9. Run python UserManager.py - This will fetch geolocation data for the call sign and update the locations table.
10. Run python TimeSlotHandler.py - This will add timeslots to the timeslots table.  - Edit and repeat this step for different days and start times
11. Update the sat name in availablepasses.py
12. Run python availablepasses.py to see if there are any passes for the upcoming week.

