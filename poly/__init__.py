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
DEFAULT_CONFIG_PATH = os.path.expanduser("~/.config/trademin/polygon.json")

## Generic functions ##


## Configuration Management ##

def load_config(config_path):
    '''
    Expects a valid path (optional) to JSON file that contains a dictionary with
    various configuration options related to polygon.io API services.

    Returns the full configuration dictionary object.
    Raises an expection is error has occurred.
    '''
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


def load_api_key_from_path(config_path):
    '''
    Expects a valid path (optional) to JSON file that contains a dictionary with
    'api_key' key and respective authentication api key value for
    Polygon API services.

    Returns the key as a str
    Raises an expection is error has occurred.
    '''
    config = load_config(config_path)
    # Load api key
    api_key = config['api_key'] if 'api_key' in config else None
    if not api_key:
        # FIXME: LOG
        print (f'api_key key undefined in {config_path}.')
    return api_key


# FIXME: Make this a generic 'save_KEY_VALUE_to_path'
# so that later we can use it to save other data to the config File
# other than just api_key without having to write a function like this
# for each one.
def save_api_key_to_path(api_key, config_path, overwrite=False):
    '''
    Expects a valid path (optional) to JSON file where the input api key string
    will be saved to a dictionary under key 'api_key' for authentication against
    Polygon.io API services.

    returns True if everything worked as expected.
    Raises an exception if error has occurred.
    '''
    if not api_key:
        raise ValueError(f"Null API key string value detected: ({api_key})")

    config_basename = os.path.basename(config_path)
    if not config_basename.split('.')[-1] == 'json':
        raise RuntimeError('config_path must point to a file with .json extension')

    # Check to see if `api_key` already exists in the config file already
    try:
        existing_api_key = load_api_key_from_path(config_path)
    except FileNotFoundError:
        # The config path does not exist, so create the path
        config_dirs = os.path.split(config_path)[0]
        os.makedirs(config_dirs)
        config = {}
    else:
        if existing_api_key and not overwrite:
            raise FileExistsError(
                f"api key already defined ({existing_api_key}). Not overwriting.")
        else:
            config = load_config(config_path)

    # Write the key:value to the config file
    # take a copy of the config file as it is now, since we only want
    # to change one parameter - then save the config again
    with open(config_path, 'w') as _config_path:
        config['api_key'] = api_key
        json.dump(config, _config_path)
    return True


## API Wrapper funtions ##

def get_marketstatus(api_key, **query_params):
    '''
    Call Polygon API `marketstatus` and print the resulting data onscreen.
    eg,
    '''
    with RESTClient(api_key) as client:
        resp = client.reference_market_status(**query_params)
    nyse = resp.exchanges['nyse']
    nasdaq = resp.exchanges['nasdaq']
    otc = resp.exchanges['otc']
    fx = resp.currencies['fx']
    crypto = resp.currencies['crypto']
    template = (f'As of {resp.serverTime}\n'
                f'  Global Crypto:\t{crypto}\n'
                f'  Global FX:\t\t{fx}\n'
                f'  US Stocks:\t\t{resp.market}\n'
                f'\tNYSE:\t\t{nyse}\n'
                f'\tNASDAQ:\t\t{nasdaq}\n'
                f'\tOTC:\t\t{otc}\n'
    )
    print(template)
    return resp
