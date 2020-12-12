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
* save key with empty key raises an exception
* save key to existing file raises an exception if overwrite == False
* save key to existing file overwrites existing file with new key if
  overwrite == True
* loading key from arbitrary file works as expected

The first commands we will wrap is `marketstatus`.
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
