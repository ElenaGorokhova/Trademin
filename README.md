This project is primarily a learning exercise, an opportunity to refresh and update knowledge about current best practices around Python and programmatic financial management and trading.

The project will evolve over time. Initially starting as a simple tool for querying various types of information from a variety of sources. This will likely be in the form of API wrappers.

As the application extends to include needed functions, more complexity will be added that aim to support the manual execution of trades and balancing of financial assets held by the user.

Then, the tool will allow for semi-automated management of trades.

Finally, the tool will enable execution of automated trading algorithms.

Meta Goals
* Learn latest Python 3 standards
* Use github to add to public project portfolio
* Take test and document first approach
* Be API centric; REST and websocket focused

Technical goals
* Python 3+ compatibility only
* Use pytest for automated regression testing
* Use plugins to extend base functionality
* Packaged and distributed via pip and docker
* Use standard library argparse for CLI
* Use JSON standard as data serialization interface and for managing CONFIG
* Use standard Python logging

Python dependencies
$> pip install polygon-api-client pytest pandas

Application description
Trademin v 0.01 will be used to execute repetitive tasks through a simple command line interface (CLI). Aka. API wrapper.

The first API we will wrap is provided by Polygon.io.

The second API we will wrap ... coming soon.
