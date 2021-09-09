import requests
import yaml

from PowerPyAPI import App
from PowerPyAPI import RestConnection


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


def authenticate_by_file(config_file):

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
        self.rest_connection = RestConnection.RestConnector(self.host, bearer_token, False, False)
        self.apps = None

    def get_apps_as_admin(self, top: int) -> [App.App]:
        json_resp = self.rest_connection.rest_call('get', 'admin/apps', query_params={'$top': top})
        ret_arr = []
        for value in json_resp['value']:
            ret_arr.append(App.App(self.rest_connection, value))
        return ret_arr

    def get_apps_by_names(self, names: [str], *, include_dev=False, include_test=False):
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

