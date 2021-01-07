#!/usr/bin/env python
'''
Poly package is a library of helper functions for communicating with Polygon.io
API services.
'''

# from IPython import embed; embed()
# import pdb; pdb.set_trace()


import datetime
import json
import os
import pytz
import re

import pandas

from polygon import RESTClient

# the default path to where Polygon.io API key is found, under key 'api_key'
DEFAULT_CONFIG_PATH = os.path.expanduser("~/.config/trademin/polygon.json")

TIMEZONES = {
    'America/New York': pytz.timezone('America/New_York')
}

## Generic functions ##
def timestamp_to_isoformat(ts):
    # FIXME: We're assuming hardcoded conversion to NEW YORK timezone from local
    dt_local = datetime.datetime.fromtimestamp(ts/1000.0)
    dt_new_york_timezone = dt_local.astimezone(TIMEZONES['America/New York'])
    dt_string = dt_new_york_timezone.isoformat()
    return dt_string

def date_parse(date_string, as_date=True):
    from dateutil.parser import parse as dtparse

    class simple_utc(datetime.tzinfo):
        def tzname(self,**kwargs):
            return "UTC"
        def utcoffset(self, dt):
            return datetime.timedelta(0)

    date_string = date_string.strip().lower()
    if date_string == 'today':
        date = datetime.datetime.utcnow()
    elif date_string == 'yesterday':
        date = datetime.datetime.utcnow() - datetime.timedelta(days=1)
    else:
        date = dtparse(date_string)

    date_tzinfo = date.replace(tzinfo=simple_utc())

    if as_date:
        date = date_tzinfo.date()
    else:
        date = date_tzinfo

    return date

def json_dump(path, data, overwrite=False):
    '''
    Dump any data to a (temporary) json file.

    Expects a valid path (optional) to JSON file where the input api key string
    will be saved to a dictionary under key 'api_key' for authentication against
    Polygon.io API services.

    returns True if everything worked as expected.
    Raises an exception if error has occurred.
    '''
    path_basename = os.path.basename(path)
    if not path_basename.split('.')[-1] == 'json':
        raise RuntimeError('path must point to a file with .json extension')

    if not (path.startswith('./') or path.startswith('/')):
        path = './' + path
        print('WARN: saving file to current working directory')

    if not data:
        raise ValueError(f"Null data object")

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
    most_recent = sorted(results, key=lambda x: date_parse(x['exDate']))[-1]

    # Check if most recent known is in the past
    next_dividend = None
    now = datetime.date.today()
    if date_parse(most_recent['exDate']).date() < now:
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
            guess_exDate_dt = date_parse(guess_result['exDate'])
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
    last_dividend = sorted(results, key=lambda x: date_parse(x['exDate']))[-1]
    return last_dividend

def get_dividends(api_key, tickers, **query_params):
    '''
    Call Polygon API `reference/dividends` for input tickers and display a
    summary of the results
    '''
    with RESTClient(api_key) as client:
        dividends = {}
        for symbol in tickers:
            symbol = symbol.upper()
            resp = client.reference_stock_dividends(symbol, **query_params)
            dividends[symbol] = {
                'count': resp.count,
                'results': resp.results,
                'last': _get_last_dividend(resp.results),
                'next': _get_next_dividend(resp.results)
                }
    return dividends

def get_ticker_aggregates(api_key, ticker, from_='yesterday', to='yesterday',
                    multiplier=1, timespan='minute', unadjusted=True,
                    sort='asc', limit=5000, **query_params):
    '''
    Polgygon.io Stock ticker Aggregates (Candles / Bars)
    GET /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to}
    EG: https://api.polygon.io/v2/aggs/ticker/AMD/range/1/minute/2021-01-04/2021-01-04?unadjusted=true&sort=asc&limit=1000&apiKey=NaOW_Dp24BpexIR8A9qADvh3owYD98Ka

    IMPORTANT: Date information is timestamped in local New York Timezone!

    Get aggregate bars for a stock over a given date range in custom time window sizes.
    For example, if timespan = ‘minute’ and multiplier = ‘5’ then 5-minute bars will be returned.

    Parameters
    ticker: (eg AMD) The ticker symbol of the stock/equity.

    multiplier: (default = 1) The size of the timespan multiplier.

    minute: (default = 'minute') The size of the time window.
            Available: minute, hour, day, week, quarter, year

    from: (eg 2021-01-04) The start of the aggregate time window.
            Available: YYYY-MM-DD or 'today' or 'yesterday'

    to: (eg 2021-01-04) The end of the aggregate time window.
            Available: YYYY-MM-DD or 'today' or 'yesterday'

    unadjusted: (default = True) Whether or not the results are adjusted for
            splits. By default, results are adjusted.
            Set this to true to get results that are NOT adjusted for splits.

    sort: (default 'asc) Sort the results by timestamp.
        Available:
          'asc' will return results in ascending order (oldest at the top)
          'desc' will return results in descending order (newest at the top).

    limit: (default = 5000) Limits the number of base aggregates queried to
        create the aggregate results.
        Polygon API Max 50000 and API Default 5000.

    JSON Response Attributes
    ticker: The exchange symbol that this item is traded under.
    status: The status of this request's response.
    adjusted: Whether or not this response was adjusted for splits.
    queryCount: The number of aggregates (minute or day) used to generate the response.
    resultsCount: The total number of results for this request.
    request_id: A request id assigned by the server.
    results:
        o: The open price for the symbol in the given time period.
        h: The highest price for the symbol in the given time period.
        l: The lowest price for the symbol in the given time period.
        c: The close price for the symbol in the given time period.
        v: The trading volume of the symbol in the given time period.
        vw: The volume weighted average price.
        t: The Unix Msec timestamp for the start of the aggregate window.
        n: The number of items in the aggregate windowAggr.
    '''
    dt_from = date_parse(from_)
    dt_to = date_parse(to)

    with RESTClient(api_key) as client:
        symbol = ticker.upper()
        resp = client.stocks_equities_aggregates(
            ticker=symbol,
            multiplier=multiplier,
            timespan=timespan,
            from_=dt_from,
            to=dt_to,
            limit=limit,
            **query_params)
        data = resp.__dict__
    return data
