class User:

    def __init__(self, rest_connection, json):
        self.app_user_access_right = json['AppUserAccessRight']
        self.email_address = json['emailAddress'] if 'emailAddress' in json else None
        self.display_name = json['displayName']
        self.identifier = json['identifier']
        self.graph_id = json['graphId']
        self.principal_type = json['principalType']
        self.rest_connection = rest_connection
