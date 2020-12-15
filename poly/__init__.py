#!/usr/bin/env python
'''
Poly package is a library of helper functions for communicating with Polygon.io
API services.
'''

from dateutil.parser import parse as dtparse
import datetime
import os
import json
import re

import pandas

from polygon import RESTClient

# the default path to where Polygon.io API key is found, under key 'api_key'
DEFAULT_CONFIG_PATH = os.path.expanduser("~/.config/trademin/polygon.json")

## Generic functions ##
def json_dump(path, data, overwrite=False):
    '''
    Dump any data to a (temporary) json file.

    Expects a valid path (optional) to JSON file where the input api key string
    will be saved to a dictionary under key 'api_key' for authentication against
    Polygon.io API services.

    returns True if everything worked as expected.
    Raises an exception if error has occurred.
    '''
    if not data:
        raise ValueError(f"Null data object")

    path_basename = os.path.basename(path)
    if not path_basename.split('.')[-1] == 'json':
        raise RuntimeError('path must point to a file with .json extension')

    # Check to see if we the file already exists
    if os.path.exists(path) and overwrite is False:
        raise FileExistsError(f"path exists ({path})")
    else:
        # The path does not exist or we want to overwrite anyway
        # Create underlying path
        dirs = os.path.split(path)[0]
        os.makedirs(dirs, exist_ok=True)

    # dump it
    with open(path, 'w') as _path:
        json.dump(data, _path)

    return True


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

def _get_next_dividend(results, guess=True):
    '''
    Input: [
        {
        'ticker': 'BAC',
        'exDate': '2013-12-04',
        'paymentDate': '2013-12-27',
        'recordDate': '2013-12-06',
        'declaredDate': '2013-10-24',
        'amount': 0.01
        }, {...} ]
    Output: Dividend datetime

    If there is a record with a date in the future from today's date,
    then it will be considered the next dividend date.

    If there is not, then we should guess (if guess is True) the next month
    when the dividend will be based on looking for the most common months
    dividends occured in the past.
    '''
    # there are no dividends to work with
    if not results:
        return None

    # grab the most recent dividend
    most_recent = sorted(results, key=lambda x: dtparse(x['exDate']))[-1]

    # Check if most recent known is in the past
    next_dividend = None
    now = datetime.date.today()
    if dtparse(most_recent['exDate']).date() < now:
        # if in the past, we can only guess when the next dividend will occur
        if guess:
            # Lets try to guess based on previous exDate's
            df = pandas.DataFrame(results).sort_values(['exDate'],
                                                       ascending=False)
            # Get all the months past dividends were executed in
            df['month'] = df.exDate.apply(lambda x: x.split('-')[1])
            # identify top 4 most common months
            most_common_months = sorted(
                df.groupby('month').count()['ticker'].sort_values(
                    ascending=False)[0:4].index.values)
            # find index of the next future month which closest to today
            this_month = datetime.datetime.now().month
            # set december to 0 value for simpler sorting
            this_month = 0 if this_month == 12 else this_month
            closest_month = sorted(most_common_months,
                key = lambda x: int(x) < this_month)[0]

            guess_result = df[
                df.exDate.str.contains('-'+closest_month+'-')].iloc[0].to_dict()
            guess_exDate_dt = dtparse(guess_result['exDate'])
            next_dividend = {
                'ticker': guess_result['ticker'],
                'guess': 1,
                'exDate': re.sub(r"^\d\d\d\d",
                                 str(guess_exDate_dt.year + 1),
                                 guess_result['exDate'])
                }
        else:
            pass # Otherwise, move on, we don't want to guess
    else:
        next_dividend = most_recent

    return next_dividend


def _get_last_dividend(results):
    if not results:
        return None
    # grab the most recent dividend
    last_dividend = sorted(results, key=lambda x: dtparse(x['exDate']))[-1]
    return last_dividend


def get_dividends(api_key, tickers, **query_params):
    '''
    Call Polygon API `reference/dividends` for input tickers and display a
    summary of the results
    '''
    with RESTClient(api_key) as client:
        dividends = {}
        for symbol in tickers:
            resp = client.reference_stock_dividends(symbol, **query_params)
            dividends[symbol] = {
                'count': resp.count,
                'results': resp.results,
                'last': _get_last_dividend(resp.results),
                'next': _get_next_dividend(resp.results)
                }
    return dividends
