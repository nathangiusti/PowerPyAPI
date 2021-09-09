from PowerPyAPI import User


class App:

    def __init__(self, rest_connection, json):
        self.id = json['id']
        self.name = json['name']
        self.last_update = json['lastUpdate']
        self.description = json['description']
        self.published_by = json['publishedBy']
        self.users = json['users']
        self.rest_connection = rest_connection

    def get_app_users(self):
        json_resp = self.rest_connection.rest_call('get', 'admin/apps/{}/users'.format(self.id))
        ret_arr = []
        for user in json_resp['value']:
            ret_arr.append(User.User(self.rest_connection, user))
        return ret_arr
