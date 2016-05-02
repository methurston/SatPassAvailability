import falcon
import UserManager
import TimeSlotHandler

api = application = falcon.API()


user = UserManager.UserAPI()
api.add_route('/user/{callsign}', user)

timeslots = TimeSlotHandler.TimeSlotAPI()
api.add_route('/user/{callsign}/timeslots', timeslots)