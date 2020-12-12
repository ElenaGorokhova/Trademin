#!/usr/bin/env python
'''
Poly package is a library of helper functions for communicating with Polygon.io
API services.
'''

import datetime
import os
import json

from polygon import RESTClient

# the default path to where Polygon.io API key is found, under key 'api_key'
DEFAULT_LINUX_CONFIG_PATH = os.path.expanduser("~/.config/trademin/polygon.json")
DEFAULT_CONFIG_PATH = DEFAULT_LINUX_CONFIG_PATH


def load_config(config_path=None):
    '''
    Expects a valid path (optional) to JSON file that contains a dictionary with
    various configuration options related to polygon.io API services.
    If no path provided, will use application default.

    Returns the full configuration dictionary object.
    Raises an expection is error has occurred.
    '''
    config_path = config_path or DEFAULT_LINUX_CONFIG_PATH
    try:
        with open(config_path) as _config_path:
            config = json.load(_config_path)
    except json.JSONDecodeError:
        if os.stat(config_path).st_size == 0:
            # FIXME: DEBUG
            print ("Config file is empty.")
            config = {}
        else:
            raise json.JSONDecodeError(f"Invalid JSON Detected. Check {config_path}.")
    return config

def save_apikey_to_path(api_key, overwrite=False, config_path=None):
    '''
    Expects a valid path (optional) to JSON file where the input api key string
    will be saved to a dictionary under key 'api_key' for authentication against
    Polygon.io API services. If no path provided, will use application default.

    returns True if everything worked as expected.
    Raises an exception if error has occurred.
    '''
    config_path = config_path or DEFAULT_LINUX_CONFIG_PATH
    if not api_key:
        raise ValueError(f"Null API key string value detected: ({api_key})")

    # Check to see if `api_key` already exists in the config file already
    existing_api_key = load_apikey_from_path(config_path)
    if existing_api_key and not overwrite:
        raise RuntimeError(
            f"api key already defined ({existing_api_key}). Not overwriting.")
    else:
        # take a copy of the config file as it is now, since we only want
        # to change one parameter - api_key - then save the config again
        config = load_config(config_path)
        with open(config_path, 'w') as _config_path:
            config['api_key'] = api_key
            json.dump(config, _config_path)


def load_apikey_from_path(config_path=None):
    '''
    Expects a valid path (optional) to JSON file that contains a dictionary with
    'api_key' key and respective authentication api key value for
    Polygon API services. If no path provided, will use application default.

    Returns the key as a str
    Raises an expection is error has occurred.
    '''
    config = load_config(config_path)
    # Load api key
    api_key = config['api_key'] if 'api_key' in config else None
    if not 'api_key' in config:
        print (f'api_key key undefined in {config_path}.')
    return api_key


def get_marketstatus(api_key, **query_params):
    print ("Market status")
    with RESTClient(api_key) as client:
        resp = client.reference_market_status(**query_params)
        print(resp.market)
    return None
