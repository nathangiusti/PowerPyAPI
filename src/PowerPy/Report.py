import PowerPyObject


class Report(PowerPyObject.PowerPyObject):
    """Power BI Report Object
    """
    def __init__(self, rest_connection: RestConnector.RestConnector, json: json) -> None:
        super().__init__(rest_connection, json)
