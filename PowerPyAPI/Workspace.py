from PowerPyAPI import Dataset


class Workspace:

    def __init__(self, rest_connection, json):
        self.id = json['id']
        self.is_read_only = json['isReadOnly']
        self.is_on_dedicated_capacity = json['isOnDedicatedCapacity']
        self.type = json['type']
        self.state = json['state']
        self.name = json['name']
        self.rest_connection = rest_connection
        if 'datasets' not in json:
            self.datasets = None
        else:
            self.datasets = self.add_datasets(json['datasets'])

    def add_datasets(self, json: dict) -> [Dataset.Dataset]:
        ret_arr = []
        for dataset in json:
            ret_arr.append(Dataset.Dataset(self.rest_connection, dataset, self))
        return ret_arr


