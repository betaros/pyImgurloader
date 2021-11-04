import json
from pathlib import Path


def get_config():
    with open(Path('config.json'), 'r') as config_file:
        return json.load(config_file)


def get_client_id():
    return get_config()['client_id']


def get_client_secret():
    return get_config()['client_secret']


def set_config(client):
    with open(Path('config.json'), 'w', encoding='utf-8') as config_file:
        json.dump(client, config_file, indent=2)

    return client
