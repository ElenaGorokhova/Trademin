#!/usr/bin/env python

import pytest

from . import poly

def test_load_config_missing_config():
    '''
    '''
    # Running with an invalid path should raise an error
    invalid_path = 'XXX'
    pytest.raises(FileNotFoundError, poly.load_config, invalid_path)

    # Running with a path know to contain something other than JSON
    # should raise json.JSONDecodeError
    # HINT: pass in a path to the READme.md file, for example

    # Running with a path known to actually point to a valid config
    # should return the contents of the JSON file (non-empty dictionary)
    # HINT: pass in the path to `fixtures/polygon.json` file

    # SKIP THIS ONE FOR NOW
    # Running with no path, when there isn't a config file already installed
    # should return an empty dictionary
    # NOTE This assumes that there isn't a config file already installed
    # Perhaps this test could just 'warn'
