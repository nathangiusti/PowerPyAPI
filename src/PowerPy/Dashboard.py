import PowerPyObject


class Dashboard(PowerPyObject.PowerPyObject):
    """Power BI Dashboard Object
    """
    def __init__(self, rest_connection: RestConnector.RestConnector, json: json) -> None:
        super().__init__(rest_connection, json)

