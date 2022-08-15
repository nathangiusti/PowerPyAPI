import requests
import Tenant


def authenticate(tenant_id: str, client_id: str, client_secret: str) -> Tenant.Tenant:
    """Authenticate against Power BI with the credentials
    Args:
        tenant_id (str): Tenant ID of Power BI instance
        client_id (str): Service principal ID
        client_secret (str): Service principal secret
    Returns:
        Tenant.Tenant: A tenant object connected to instance
    """
    data = {
        'client_id': client_id,
        'grant_type': 'client_credentials',
        'resource': 'https://analysis.windows.net/powerbi/api',
        'response_mode': 'query',
        'client_secret': client_secret
    }
    resp = requests.get('https://login.microsoftonline.com/{}/oauth2/token'.format(tenant_id), data=data)
    return Tenant(resp.json()['access_token'])


def authenticate_by_file(config_file: str) -> Tenant.Tenant:
    """Authenticate against Power BI with credentials in config file

    Config file should be yaml format
    client_id: <client_id>
    client_secret: <client_secret>
    tenant_id: <tenant_id>

    Args:
        config_file (str): Path to config file
    Returns:
        Tenant.Tenant: A tenant object connected to instance
    """
    with open(config_file, 'r') as yml_file:
        cfg = yaml.safe_load(yml_file)

        tenant_id = cfg['tenant_id'] if 'tenant_id' in cfg else False
        client_id = cfg['client_id'] if 'client_id' in cfg else True
        client_secret = cfg['client_secret'] if 'client_secret' in cfg else None

        return authenticate(tenant_id, client_id, client_secret)
