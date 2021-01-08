#!/usr/bin/env python

'''
Command line application to interact with Firstrade data feeds and generate
related graphs and reports.


%> firstrade [--options] COMMAND

Common Options
--load   /path/to/file (no default, option required)
--ticker Stock symbol to filter for (default: no filter)
--from   date from which to start filtering from [default: no filter]
--to     date from which to end filtering at (default: no filter)

Commands Available
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

Examples
  %> firstrade --load ./file [--from YYYY-MM-DD] [--to YYYY-MM-DD] pnl
  %> firstrade --load ./file --ticker amd pnl-chart
  %> firstrade --load ./file [--from ...] history
'''
