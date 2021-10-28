import json


def get_config():
    with open('config.json') as config_file:
        return json.load(config_file)


def get_client_id():
    return get_config()['client_id']


def get_client_secret():
    return get_config()['client_secret']


def set_config(client_id, client_secret):
    return None
