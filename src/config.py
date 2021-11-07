import json
from pathlib import Path

from src.utils import get_project_root


def get_config():
    root = get_project_root()
    with open(Path(root, 'config.json'), 'r') as config_file:
        return json.load(config_file)


def get_client_id():
    return get_config()['client_id']


def get_client_secret():
    return get_config()['client_secret']


def set_config(client):
    root = get_project_root()
    with open(Path(root, 'config.json'), 'w', encoding='utf-8') as config_file:
        json.dump(client, config_file, indent=2)

    return client
