#TODO

## General
* Implement logging
 - Add --debug option to trademin-poly.py

## trademin-poly
First application will be a command line interface (CLI) that allows us to
make queries and run commands related against the Polygon.io API.

We will create a Polygon python package (__init__.py) in a folder and a
script using `argparse` module to manage the CLI commands and options.

First, we need to be able to save and load our Polygon.io API key from a
config file stored locally on our system.
--
$> trademin-poly [--config $CONFIG_FILE] configure --api-key $APIKEY_STRING [--overwrite]
$> trademin-poly [--config $CONFIG_FILE]
--

Default location for $CONFIG_FILE (JSON) will be
  [$USERHOME]/.config/trademin/polygon.json

API key will be saved under the dictionary key 'api_key'

Tests required:
* save key to user defined CONFIG_FILE works as expected
* save key with NULL (empty) key raises an exception
* save key to existing file raises an exception if overwrite == False
* save key to existing file overwrites existing file with new key if
  overwrite == True
* loading key from arbitrary file works as expected

The first commands we will wrap is `marketstatus` (v2/marketstatus/now). eg,
```
$> trademin-poly marketstatus
[ 2020-12-11T06:21:33-05:00 ]
US Stocks:     Extended Hours
US Exchanges
  NYSE:        Extended Hours
  NASDAQ:      Extended Hours
  OTC:         Extended Hours
Global Crypto: Open
Global FX:     Open
```

No tests required at this time for the `trademin-poly` application itself.

Another command to implement is `dividends` (v2/reference/dividends). eg,
```
$> trademin-poly dividends BAC [UBER]
Bank of America (BAC) summary
  Total: 62 (since 1988-11-21)

  Next: Unannounced
    Estimated:    2020-08-09

  Last:    
    Ex date:      2020-11-06
    Record date:  2020-11-09
    Payment date: 2020-11-12

--

Uber Technologies (UBER) summary
  Total: 0

  Next: UNKNOWN

  Last: UNKNOWN
```

Then we'll try to start loading data. Initially, Aggregate candles (v2/aggs/ticker).
The data will just be dumped as JSON for now.

```
$> trademin-poly aggregates BAC
```
