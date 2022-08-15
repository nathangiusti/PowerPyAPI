import PowerPyObject


class Dataflow(PowerPyObject.PowerPyObject):
    """Power BI Dataflow Object
    """
    def __init__(self, rest_connection: RestConnector.RestConnector, json: json) -> None:
        super().__init__(rest_connection, json)
