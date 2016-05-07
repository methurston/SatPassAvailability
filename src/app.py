import falcon
import UserManager
import TimeSlotHandler
import TleHandler
import AvailablePasses

api = application = falcon.API()
TleHandler.UpdateTLE()

user = UserManager.UserAPI()
api.add_route('/user/{callsign}', user)
# PUT  Add or Update a user.
# Body:
# {
#     "lat": ,
#     "long": ,
#     "timezone": "America/Boise",
#     "street_address": null
# }
# If using a US Callsign,  send lat, long, and street address as null.
# Otherwise send lat, long, or street_adress
#
# GET  Returns stored data for a callsign.

timeslots = TimeSlotHandler.TimeSlotAPI()
api.add_route('/user/{callsign}/allslots', timeslots)
# PUT  Add a new availabilty timeslot.
# Body:
# {
#     "days": ,
#     "start_time": ,
#     "duration"
# }
# GET
# Returns an expansion of the next week of time slots.


slotwithpass = AvailablePasses.AvailablePassAPI()
api.add_route('/user/{callsign}/availablepass', slotwithpass)
# GET
# Query Paramters:
# sat_list = comma separated list of satellite names (no spaces).
# min_elevation = Minimum elevation (in degrees) to consider a pass valid.  If this is omitted, any pass over 0 degrees
# will be returned.
# Returns any upcoming pass that conincides with the list returned by GETting allslots
