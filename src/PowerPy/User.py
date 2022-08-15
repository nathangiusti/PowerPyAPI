import PowerPyObject


class User(PowerPyObject.PowerPyObject):
    """Power BI User Object
    """
    def __init__(self, rest_connection: RestConnector.RestConnector, json: json) -> None:
        super().__init__(rest_connection, json)

