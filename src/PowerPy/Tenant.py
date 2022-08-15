import App
import RestConnector
import Workspace


class Tenant:

    def __init__(self, bearer_token: str):
        self.host = 'https://api.powerbi.com/v1.0/myorg'
        self.rest_connection = RestConnector.RestConnector(self.host, bearer_token, False, False)
        self.apps = None
        self.workspaces = None

    def get_apps(self, *, top: int = 5000, force_refresh: bool = False, names: [str]) -> [App.App]:
        """Gets apps
        Args:
            top (int): (Optional) Number of apps to return. Between 1 and 5000. Default 5000
            force_refresh (bool): (Optional) To reduce API usage results from previous calls are cashed. Set True to force refresh from service. Default False
            names ([str]): (Optional) A list of app names to return
        Returns:
            [App]: An array of App objects
        """
        ret_arr = []
        if force_refresh or self.apps is None:
            json_resp = self.rest_connection.rest_call('get', 'admin/apps', query_params={'$top': top})
            ret_arr = []
            for value in json_resp['value']:
                ret_arr.append(App.App(self.rest_connection, value))
            self.apps = ret_arr

        if names is not None:
            ret_arr = []
            for app in self.apps:
                if app.name in names:
                    ret_arr.append(app)

        return ret_arr

    def get_workspaces(self, *, top: int = 5000) -> [Workspace.Workspace]:
        """Gets workspaces
        Args:
            top (int): (Optional) Number of workspaces to return. Between 1 and 5000. Default 5000
        Returns:
            [Workspace.Workspace]: An array of workspace objects
        """
        query_params = {
            '$filter': 'type eq \'Workspace\'',
            '$top': top
        }
        ret_arr = []
        response_json = self.rest_connection.rest_call('get', 'admin/groups', query_params=query_params)
        for workspace in response_json['value']:
            ret_arr.append(Workspace.Workspace(self.rest_connection, workspace))
        return ret_arr

    def get_datasets(self, *, top: int = 5000) -> [Dataset.Dataset]:
        """Gets datasets
        Args:
            top (int): (Optional) Number of datasets to return. Between 1 and 5000. Default 5000
        Returns:
            [Dataset.Dataset]: An array of dataset objects
        """
        query_params = {
            '$filter': 'type eq \'Workspace\'',
            '$top': top,
            '$expand': 'datasets'
        }
        ret_arr = []
        response_json = self.rest_connection.rest_call('get', 'admin/groups', query_params=query_params)
        for dataset in response_json['value']:
            ret_arr.append(Dataset.Dataset(self.rest_connection, dataset))
        return ret_arr

    def get_all_workspace_info(self, *, top: int = 5000, names: [str] = None, force_refresh: bool = False) \
            -> [Workspace.Workspace]:
        """Gets all available info for workspaces
        Args:
            top (int): (Optional) Number of workspaces to return. Between 1 and 5000. Default 5000
            force_refresh (bool): (Optional) To reduce API usage results from previous calls are cashed. Set True to force refresh from service. Default False
            names ([str]): (Optional) A list of workspace names to return
        Returns:
            [App]: An array of App objects
        """
        query_params = {
            '$filter': 'type eq \'Workspace\'',
            '$top': top,
            '$expand': 'datasets,users,reports,dashboards,datasets,dataflows,workbooks'
        }

        if force_refresh or self.workspaces is None:
            ret_arr = []
            response_json = self.rest_connection.rest_call('get', 'admin/groups', query_params=query_params)
            i = 0
            for workspace in response_json['value']:
                i += 1
                ret_arr.append(Workspace.Workspace(self.rest_connection, workspace))
            self.workspaces = ret_arr

        if names is None:
            return self.workspaces
        else:
            ret_arr = []
            for workspace in self.workspaces:
                if workspace.name in names:
                    ret_arr.append(workspace)
        return ret_arr
