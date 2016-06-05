import falcon
import UserManager
import TimeSlotHandler
import TleHandler
import AvailablePasses
# import requests

ALLOWED_ORIGINS = ['http://localhost:8080']
ALLOWED_METHODS = ['GET', 'POST', 'DELETE']
ALLOWED_HEADERS = ['Content-Type']


class CorsMiddleware(object):
    """stolen from http://hpincket.com/falcon-framework-cors-for-no-access-control-allow-origin.html"""

    def process_request(self, request, response):
        response.set_header('Access-Control-Allow-Headers', ','.join(ALLOWED_HEADERS))
        response.set_header('Access-Control-Allow-Methods', ','.join(ALLOWED_METHODS))
        origin = request.get_header('Origin')
        method = request.method
        if origin in ALLOWED_ORIGINS:
            response.set_header('Access-Control-Allow-Origin', origin)
        # if method in ALLOWED_METHODS:
        #     print('Method: {}'.format(method))
        #     response.set_header('Access-Control-Allow-Methods', method)


api = application = falcon.API(middleware=CorsMiddleware())
TleHandler.UpdateTLE()

user = UserManager.UserAPI()
api.add_route('/user/{callsign}', user)
# PUT  Add or Update a user.
# Body:
# {
#     "lat": ,  # Latitude
#     "long": , # Longitude
#     "timezone": , # Any standard name for a timezone, e.g. "America/Denver" US/Eastern or UTC.
#     "street_address": # USed if you don't send a US Callsign.  A geocode lookup will generate Lat/Lon.
# }
#
# If using a US Callsign,  sending lat, long, and street address as null will force a lookup via callook.info.
# Sending a street address will force a geocode lookup
#
# GET  Returns stored data for a callsign.


timeslots = TimeSlotHandler.TimeSlotAPI()
api.add_route('/user/{callsign}/allslots', timeslots)
# POST  Add a new availabilty timeslot.
# Body:
# {
#     "days": ,  # Send a list of the days you are available.
#     "start_time": ,  #24 our clock, server assumes this is timezone associated with the callsign.
#     "duration": # Amount of time to check for passes in seconds.
# }
# GET
# Returns an expansion of the next week of time slots.

singleslot = TimeSlotHandler.TimeSlotAPI()
api.add_route('/user/{callsign}/allslots/{reqid}', timeslots)
# DELETE
# Deletes a stored timeslot by id.

slotwithpass = AvailablePasses.AvailablePassAPI()
api.add_route('/user/{callsign}/availablepass', slotwithpass)
# GET
# Query Paramters:
# sat_list = comma separated list of satellite names (no spaces).
# min_elevation = Minimum elevation (in degrees) to consider a pass valid.  If this is omitted, any pass over 0 degrees
# will be returned.
# Returns any upcoming pass that conincides with the list returned by GETting allslots

allsats = TleHandler.SatHandlerApi()
api.add_route('/satellites', allsats)
# GET
# Returns a distinct list of satellite names in an array
