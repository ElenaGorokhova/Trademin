#!/usr/bin/env python
'''
# Firstrade CLI
Command line application to interact with Firstrade data feeds and generate
related graphs and reports.

```
%> firstrade.py [--options] COMMAND
Commands: pnl, pnl-chart, withdrawals

Options:
--load   /path/to/file (no default, option required)
--ticker Stock symbol to filter for (default: no filter)
--from   date from which to start filtering from [default: no filter]
--to     date from which to end filtering at (default: no filter)
```

## Commands Available
* `pnl`: diplays summary of Profit and Loss information for given timeframe

    Summary for AMD from DATE to DATE
      Bought     : -$ZZZZ (SHARE COUNT)
      Sold       : +$WWWW (SHARE COUNT)
    ----------------------------------
      Gross PNL  : [+-]$$$$$
    ----------------------------------
      Fees       : -:(:(:(
      Commissions: -:-0:-0:-0
      Dividends  : +:):):):)
    ----------------------------------
      Net PNL    : [+-]$$$

* `pnl-chart`: generates chart showing PnL over time

* `withdrawals`: displays summary of withdrawal activity (ie, 'Other: ACH DISBURSEMENT')

## Examples
`%> firstrade.py --load ./file.csv [--from YYYY-MM-DD] [--to YYYY-MM-DD] pnl`
`%> firstrade.py --load ./file.csv --ticker amd pnl-chart`
`%> firstrade.py --load ./file.csv withdrawals`

    Withdrawal Summary from DATE to DATE
      YYYY-MM-DD  : $XXXX
      YYYY-MM-DD  : $ZZZZ
    ------------------------------------
    Total : $:):):):)~


### Idea
Command: `cache --load ./file`: Import data in ./file.csv to local SQLite db
Notes:
* Save the DB here: DEFAULT_FT_DB = os.path.join(poly.DEFAULT_USER_PATH, 'firstrade.db'
* --load would no longer be required. Default would be to load from DB)
* More information about sqlite (+ pandas)
 https://datacarpentry.org/python-ecology-lesson/09-working-with-sql/index.html

## Development Suggestions
* Separate your code into functional units whenever parts are clearly
  reusable in other places.

1 Start with creating the working command line app with `argparse` such that
  `firstrade.py --help` returns without error. HINT: if '__name__' == '__main__'
2 Create a 'load' option which when present loads the file provided and
  returns a Dataframe that will be used later on by other functions
3 Add the withdrawals command (using the dataframe as input created by the load
  coded before)
4 Add `pnl` command and a function to process the pnl and return a new dataframe
  with pnl data (with input being the dataframe prepared previously) eg,
  [{'symbol': 'AMD', from:'DATE', to:'DATE', bought': xxx, 'sold': xxx, 'gross_pnl': ...}]
5 Given that data, display the output to the screen
6 Then try to add the other options / filters (symbol, from, to)
7 Then try to generate a line graph showing the cumulative PnL over time
  eg, https://seasonaltrader.com/ST_Help/Content/Resources/Images/Capture7.jpg
'''

# This code here allows us to `import poly` even if it is not properly installed
# and instead we are simply running from within the repository locally
try:
    # Poly is already in the system path, import as usual
    import poly
except ImportError:
    # This script is being run from the repository directly probably, just
    # check the parent directory for the packages instead
    PACKAGE_PARENT = '..'
    SCRIPT_DIR = os.path.dirname(
        os.path.realpath(
            os.path.join(os.getcwd(), os.path.expanduser(__file__))))
    sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
    import poly


# For more info, see: https://docs.python.org/3/library/argparse.html
import argparse

# HAVE FUN! :)
