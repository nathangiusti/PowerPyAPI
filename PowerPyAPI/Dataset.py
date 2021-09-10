from __future__ import annotations

from PowerPyAPI import RestConnector, User, Workspace


class Dataset:

    def __init__(self, rest_connection: RestConnector.RestConnector, json: dict, workspace: Workspace.Workspace = None):
        self.workspace = workspace
        self.rest_connection = rest_connection
        self.id = json['id']
        self.name = json['name']
        self.add_rows_api_enabled = json['addRowsAPIEnabled']
        self.is_refreshable = json['isRefreshable']
        self.is_effective_identity_required = json['isEffectiveIdentityRequired']
        self.is_effective_identity_roles_required = json['isEffectiveIdentityRolesRequired']
        self.target_storage_mode = json['targetStorageMode']
        self.created_date = json['createdDate']
        self.content_provider_type = json['contentProviderType']
        self.upstream_datasets = []
        for dataset in json['upstreamDatasets']:
            self.upstream_datasets.append(Dataset(rest_connection, dataset, None))
        self.schema_may_not_be_up_to_date = json['schemaMayNotBeUpToDate']
        self.users = []
        for user in json['users']:
            self.users.append(User.User(rest_connection, user))

