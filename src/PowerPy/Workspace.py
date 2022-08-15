import json

import Dataset
import PowerPyObject


class Workspace(PowerPyObject.PowerPyObject):
    """Power BI Workspace Object
    """
    def __init__(self, rest_connection: RestConnector.RestConnector, json: json) -> None:
        super().__init__(rest_connection, json)