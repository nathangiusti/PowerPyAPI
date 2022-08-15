import PowerPyObject


class Dataset(PowerPyObject.PowerPyObject):
    """Power BI Dataset Object
    """
    def __init__(self, rest_connection: RestConnector.RestConnector, json: json) -> None:
        super().__init__(rest_connection, json)
