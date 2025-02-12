import json
import requests
import shutil
import urllib.parse


class RestConnector:
    """The REST Wrapper for PowerPy
    Use the rest_call method to make calls to the API
    Attributes:
        host (str): The host string, the base of the url to call
        debug (bool): Whether to print debug messages about rest requests
        verify (bool): Whether to use SSL Certificate Verification
        token (JSON): The authorization header
    """

    def __init__(self, host: str, token: str, debug: bool, verify: bool):
        """
        Args:
            host (str): The host string, the base of the url to call
            debug (bool): Whether to print debug messages about rest requests
            verify (bool): Whether to use SSL Certificate Verification
            token (JSON): The authorization token
        """
        self.host = host
        self.debug = debug
        self.verify = verify
        self.token = {
            'Authorization': 'Bearer {}'.format(token)
        }

    def rest_call(self, action_type: str, url: str, *,
                  data: Any = None, json_payload: json = None, query_params: dict[str, Any] = None,
                  path: str = None, file: str = None, raw: bool = False) -> json:
        """Run an arbitrary rest command against PowerBI tenant
        Args:
            action_type (str): REST request type (get, post, patch, put, delete)
            url (str): api end point, example api/v1/app_database/encrypt_database_password or api/branding
            data (Any): (Optional) The data portion of the payload
            json_payload (JSON): (Optional) The JSON portion of the payload
            query_params (dict[Str,Any]): (Optional) A dictionary of query values to be added to the end of the url
                Method will strip out None dictionary values.
            path (str): (Optional) If set, response will be downloaded to file path
            file (str): (Optional) Path to files to be uploaded. Only usable with post.
            raw (bool): (Optional) If true, write raw data to file. Writes JSON by default
        Returns:
            JSON: Returns the json content blob by default. If path is set, returns nothing
        """

        action_type = action_type.lower()
        if query_params is not None:
            query_string = build_query_string(query_params)
        else:
            query_string = ''
        full_url = '{}/{}{}'.format(self.host, url, query_string)

        if self.debug:
            print('{}: {}'.format(action_type, full_url))
            if data is not None:
                print('Data: {}'.format(data))
            if json_payload is not None:
                print('JSON: {}'.format(json_payload))

        if file is not None:
            if action_type != 'post':
                raise Exception('Files can only be uploaded via post')
            file = {'file': open(file, 'rb')}

        if path is not None:
            with requests.request(
                action_type, full_url, stream=True,
                headers=self.token, data=data, json=json_payload, verify=self.verify
            ) as response:
                if raw:
                    with open(path, 'wb') as f:
                        shutil.copyfileobj(response.raw, f)
                else:
                    json.dump(response.json(), open(path, 'wb'))
        else:
            response = requests.request(
                action_type, full_url,
                headers=self.token, data=data, json=json_payload, verify=self.verify, files=file
            )
            parse_response(response)
            if len(response.content) == 0:
                return None
            else:
                try:
                    return response.json()
                except ValueError as e:
                    return response.content

    def simple_rest_call(self, action_type: str, url: str) -> json:
        """Simplified rest call when advanced options are unnecessary.
        Args:
            action_type (str): REST request type (get, post, patch, put, delete)
            url (str): api end point, example api/v1/app_database/encrypt_database_password or api/branding
        Returns:
            JSON: Returns the json content blob by default. If path is set, returns nothing
        """
        action_type = action_type.lower()
        full_url = url
        if self.debug:
            print('{}: {}'.format(action_type, full_url))
        response = requests.request(action_type, full_url, headers=self.token, verify=self.verify)
        parse_response(response)
        if len(response.content) == 0:
            return None
        else:
            try:
                return response.json()
            except ValueError as e:
                return response.content


def parse_response(response: requests.Response) -> None:
    """Parses response and throw exception if not successful."""
    if response.status_code not in [200, 201, 204]:
        raise Exception('ERROR: {}: {}\nURL: {}'.format(response.status_code, response.content, response.url))


def build_query_string(dictionary: dict[str, Any]) -> str:
    """Builds a query string based on the dictionary passed in"""

    ret_arr = []
    separator = '&'
    for key, value in dictionary.items():
        if value is not None:
            if isinstance(value, bool):
                if value is True:
                    validated = 'true'
                elif value is False:
                    validated = 'false'
            elif isinstance(value, list):
                validated = ','.join(value)
            else:
                if key != 'query':
                    validated = urllib.parse.quote(str(value))
                else:
                    validated = str(value)
            ret_arr.append("{}={}".format(key, validated))
    query_string = separator.join(ret_arr)
    if len(query_string) > 1:
        return '?' + query_string
    else:
        return ''
