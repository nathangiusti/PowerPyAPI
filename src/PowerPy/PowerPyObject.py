import json

import RestConnector


class PowerPyObject:
    def __init__(self, rest_connection: RestConnector.RestConnector, json: json) -> None:
        self.json = json
        self.rest_connection = rest_connection
