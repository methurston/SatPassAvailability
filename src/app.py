import falcon
import UserManager

api = application = falcon.API()


user = UserManager.UserAPI()
api.add_route('/user/{callsign}', user)
