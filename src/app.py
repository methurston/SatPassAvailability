import falcon
import UserManager
import TimeSlotHandler
import TleHandler
import AvailablePasses

api = application = falcon.API()
TleHandler.UpdateTLE()

user = UserManager.UserAPI()
api.add_route('/user/{callsign}', user)

timeslots = TimeSlotHandler.TimeSlotAPI()
api.add_route('/user/{callsign}/allslots', timeslots)

slotwithpass = AvailablePasses.AvailablePassAPI()
api.add_route('/user/{callsign}/availablepass', slotwithpass)
