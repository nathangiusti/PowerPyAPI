import PowerPyObject

import User


class App(PowerPyObject.PowerPyObject):
    """Power BI App Object
    """
    def __init__(self, rest_connection: RestConnector.RestConnector, json: json) -> None:
        super().__init__(rest_connection, json)

    def get_app_users(self) -> [User.User]:
        """Gets all users of an app
        Returns:
            JSON: Returns the json content blob by default. If path is set, returns nothing
        """
        json_resp = self.rest_connection.rest_call('get', 'admin/apps/{}/users'.format(self.id))
        ret_arr = []
        for user in json_resp['value']:
            ret_arr.append(User.User(self.rest_connection, user))
        return ret_arr
