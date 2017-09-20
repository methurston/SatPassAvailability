# Sat Pass Availability 
Under documented and barely tested proof of concept where a user can find out if an amateur radio satellite pass is going to occur when the user (location) is available.

There are 3 main data objects.

1. Satellite Info (tlehandler.py)- This is stored in two line element format.  The information is retrieved from amsat or celestrak.

2. Location (UserManager.py) - This is geo information about a user using a unique identifier (usually callsign).  Lat/Lon information comes from callook.info, elevation is pulled from google's geocode API.

3. Timeslot (TimeSlotHandler.py) - Timeslots are the times a location is available to catch a satellite pass.


SatTrack.py puts all of the information together and uses PyEphem to calculate the next pass from a given time, lat, lon, and elevation.  This will then spit out a list of potential good passes when the location is available to work the sat.


# Instructions
It's recommended to set up a Python 2.7 or 3.5 virtualenv for use. As of writing, both versions are supported,
Version 3.5 will be the primary version supported going forward.

1. Clone this repo.
2. Install the required libraries via pip (pip install --upgrade -r requriements.txt)
3. Run the config generator (**python configbuilder.py**).

    This script will search the file structure for existing sqlite3 databases, if none are found a new database
will be generated and an empty schema will be applied.
*Note: Schema will not be validated if existing file is used*

4. To run a test version locally, run src/tests/testlauncher.py.  This will launch the API on port 8000 and the UI on port 8181.


#TODO:
1. Consider implementing Schema control.
2. Wrap the whole damn thing in flask and make it a rest API. -DONE.  Using falcon for the API framework
3. Add auth.
4. Add Insert Date/Time stamp for users.  Implement a method to update if time threshold has expired.
5. Consider using Dynamo as datastore instead of a dedicated RDS.
6. Convert to lambda/api gateway or other serverless architecture.

#Issues:
For some reason calculations for AO-85 are slightly off from the pass prediction on amsat.org. SO-50 and ISS match predictions.

Max elevation AZ is not matching amsat. It seems to match other sources.
