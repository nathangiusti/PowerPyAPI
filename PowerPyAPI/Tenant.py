import requests
import yaml

from PowerPyAPI import Activity, App, RestConnector, Workspace


def generate_bearer_token(tenant_id: str, client_id: str, client_secret: str):
    data = {
        'client_id': client_id,
        'grant_type': 'client_credentials',
        'resource': 'https://analysis.windows.net/powerbi/api',
        'response_mode': 'query',
        'client_secret': client_secret
    }
    resp = requests.get('https://login.microsoftonline.com/{}/oauth2/token'.format(tenant_id), data=data)

    return resp.json()['access_token']


def authenticate_by_file(config_file: str):
    with open(config_file, 'r') as yml_file:
        cfg = yaml.safe_load(yml_file)

        token = cfg['token'] if 'token' in cfg else None
        tenant_id = cfg['tenant_id'] if 'tenant_id' in cfg else False
        client_id = cfg['client_id'] if 'client_id' in cfg else True
        client_secret = cfg['client_secret'] if 'client_secret' in cfg else None

        if token is None:
            return Tenant(generate_bearer_token(tenant_id, client_id, client_secret))
        else:
            return Tenant(token)


class Tenant:

    def __init__(self, bearer_token: str):
        self.host = 'https://api.powerbi.com/v1.0/myorg'
        self.rest_connection = RestConnector.RestConnector(self.host, bearer_token, False, False)
        self.apps = None

    def get_apps_as_admin(self, top: int = 5000) -> [App.App]:
        json_resp = self.rest_connection.rest_call('get', 'admin/apps', query_params={'$top': top})
        ret_arr = []
        for value in json_resp['value']:
            ret_arr.append(App.App(self.rest_connection, value))
        return ret_arr

    def get_apps_by_names(self, names: [str], *, include_dev: bool = False, include_test: bool = False) -> [App.App]:
        if self.apps is None:
            self.apps = self.get_apps_as_admin(5000)

        name_len = len(names)
        if include_dev:
            for i in range(0, name_len):
                names.append(names[i] + " [Dev]")
        if include_test:
            for i in range(0, name_len):
                names.append(names[i] + " [Test]")
        ret_arr = []
        for app in self.apps:
            if app.name in names:
                ret_arr.append(app)

        return ret_arr

    def get_workspaces(self, top: int = 5000) -> [Workspace.Workspace]:
        query_params = {
            '$filter': 'type eq \'Workspace\'',
            '$top': top
        }
        ret_arr = []
        response_json = self.rest_connection.rest_call('get', 'admin/groups', query_params=query_params)
        for workspace in response_json['value']:
            ret_arr.append(Workspace.Workspace(self.rest_connection, workspace))
        return ret_arr

    def get_datasets(self, top: int = 5000):
        query_params = {
            '$filter': 'type eq \'Workspace\'',
            '$top': top,
            '$expand': 'datasets'
        }
        ret_arr = []
        response_json = self.rest_connection.rest_call('get', 'admin/groups', query_params=query_params)
        for workspace in response_json['value']:
            ret_arr.append(Workspace.Workspace(self.rest_connection, workspace))
        return ret_arr

"""
    def get_activities(self, start_date, end_date):
        query_params = {
            'startDateTime': '\'' + start_date + '\'',
            'endDateTime': '\'' + end_date + '\''
        }
        json = self.rest_connection.rest_call('get', 'admin/activityevents', query_params=query_params)
        continuation_token = ''
        ret_arr = {}
        while True:
            for activity in json['activityEventEntities']:
                key_arr = []
                if activity['Activity'] not in ret_arr:
                    for key in activity.keys():
                        key_arr.append(key)
                    ret_arr[activity['Activity']] = key_arr

                #ret_arr.append(Activity.Activity(self.rest_connection, activity))
            if json['continuationToken'] is None:
                break
            json = self.rest_connection.simple_rest_call('get', json['continuationUri'])
        return ret_arr
    """
