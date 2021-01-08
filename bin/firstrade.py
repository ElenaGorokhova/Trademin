#!/usr/bin/env python
'''
# Firstrade CLI
Command line application to interact with Firstrade data feeds and generate
related graphs and reports.

`%> firstrade [--options] COMMAND`

## Common Options
`--load   /path/to/file (no default, option required)`
`--ticker Stock symbol to filter for (default: no filter)`
`--from   date from which to start filtering from [default: no filter]`
``--to     date from which to end filtering at (default: no filter)`

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

* `history`: generates chart showing entry and exit points for all Buy/Sell orders

## Examples
`%> firstrade --load ./file.csv [--from YYYY-MM-DD] [--to YYYY-MM-DD] pnl`
`%> firstrade --load ./file.csv --ticker amd pnl-chart`
`%> firstrade --load ./file.csv [--from ...] history`

## Idea
Command:
`cache --load ./file`: Import data in ./file.csv to local SQLite db
(DEFAULT_FT_DB = os.path.join(poly.DEFAULT_USER_PATH, 'firstrade.db')
(NOTE: --load would no longer be required. Default would be to load from DB)
'''

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
