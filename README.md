# Sat Pass Availability 
Under documented and barely tested proof of concept where a user can find out if an amateur radio satellite pass is going to occur when the user (location) is available.

There are 3 main data objects.

1. Satellite Info (tlehandler.py)- This is stored in two line element format.  The information is retrieved from amsat or celestrak.

2. Location (UserManager.py) - This is geo information about a user using a unique identifier (usually callsign).  Lat/Lon information comes from callook.info, elevation is pulled from google's geocode API.


3. Timeslot (TimeSlotHandler.py) - Timeslots are the times a location is available to catch a satellite pass.


SatTrack.py puts all of the information together and uses PyEphem to calculate the next pass from a given time, lat, lon, and elevation.  This will then spit out a list of potential good passes when the location is available to work the sat.


# Instructions
It's recommended to set up a Python 2.7 virtualenv for use.

1. Clone this repo.
2. Install the required libraries via pip (pip install --upgrade -r requriements.txt)
3. Run the config generator (**python configbuilder.py**).

    This script will search the file structure for existing sqlite3 databases, if none are found a new database
will be generated and an empty schema will be applied.
*Note: Schema will not be validated if existing file is used*

4. Insert satellite TLE info (**python src/tlehandler.py**).]

    This script will pull the latest TLE info from amsat.org and load it into the DB.

5. Insert location data about the user (**python src/UserManager.py**).

    This script looks up callsign info from callook.info to get Lat and Long for the callsign's QTH data.
Then it uses that Lat/Long to get the elevation from Google.

6. Edit the example timeslot in src/TimeSlotHandler.py to list a single availability.

    The structure of the data is:

    `callsign:` Must be a user in the DB, Defaults to value in config.json

    `days:`  A list days that the user has available.  Example: 'Sat, Sun,M,T,W,Th,F'.

    `start time:` The starting time (24h) the user has available. Examlple: '21:00'.

    `duration:` The amount of time the user has available in seconds.  Example: '4800'.


7. Populate the timeslots in the database (**python src/TimeSlotHandler.py**).

    Repeat this step to add different start times.

8. Update the satellite names on line 63 of availablepasses.py
9. Run python availablepasses.py to see if there are any passes for the upcoming week.

#TODO:
1. Consider implementing -ORM- and Schema control.
   Status: ORM integration (peewee) complete.  Schema control TBD
2. Wrap the whole damn thing in flask and make it a rest API.
3. Return valid JSON with human readable values for each item.  (Required for #3)

#Issues:
For some reason calculations for AO-85 are slightly off from the pass prediction on amsat.org. SO-50 and ISS match predictions.

Max elevation AZ is not matching amsat. It seems to match other sources.
