import PowerPyObject
import Dashboard
import Dataflow
import Dataset
import Report
import User
import Workbook


class Workbook(PowerPyObject.PowerPyObject):
    """Power BI Workbook Object
    """
    def __init__(self, rest_connection: RestConnector.RestConnector, json: json) -> None:
        super().__init__(rest_connection, json)
        self.datasets = self.add_datasets(json['datasets'])
        self.users = self.add_users(json['users'])
        self.reports = self.add_reports(json['reports'])
        self.dashboards = self.add_dashboards(json['dashboards'])
        self.dataflows = self.add_dataflows(json['dataflows'])
        self.workbooks = self.add_workbook(json['workbooks'])

    def add_datasets(self, json: dict) -> [Dataset.Dataset]:
        ret_arr = []
        for dataset in json:
            ret_arr.append(Dataset.Dataset(self.rest_connection, dataset, self))
        return ret_arr

    def add_users(self, json: dict) -> [User.User]:
        ret_arr = []
        for user in json:
            ret_arr.append(User.User(self.rest_connection, user))
        return ret_arr

    def add_reports(self, json: dict) -> [Report.Report]:
        ret_arr = []
        for report in json:
            ret_arr.append(Report.Report(self.rest_connection, report, self))
        return ret_arr

    def add_dashboards(self, json: dict) -> [Dashboard.Dashboard]:
        ret_arr = []
        for report in json:
            ret_arr.append(Dashboard.Dashboard(self.rest_connection, report, self))
        return ret_arr

    def add_dataflows(self, json: dict) -> [Dataflow.Dataflow]:
        ret_arr = []
        for report in json:
            ret_arr.append(Dataflow.Dataflow(self.rest_connection, report, self))
        return ret_arr

    def add_workbook(self, json: dict) -> [Workbook.Workbook]:
        ret_arr = []
        for report in json:
            ret_arr.append(Workbook.Workbook(self.rest_connection, report, self))
        return ret_arr