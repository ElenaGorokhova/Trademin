# trademin-poly

This application is a command line interface (CLI) that allows us to
make queries and run commands related against the Polygon.io API.

It is a python package (`poly/__init__.py`) and consists of library functions
and scripts that use `argparse` module to manage the CLI commands and options.

First off, its able able to save and load our Polygon.io API key from a
config file stored locally on our system.

```
$> trademin-poly [--config $CONFIG_FILE] configure --api-key $APIKEY_STRING [--overwrite]
$> trademin-poly [--config $CONFIG_FILE]
```

Default location for $CONFIG_FILE (JSON) is: `[$USERHOME]/.config/trademin/polygon.json`

API key will be saved under the dictionary key 'api_key'.

It wraps `marketstatus` (v2/marketstatus/now). eg,
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


Another command implemented is `dividends` (v2/reference/dividends). eg,
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
