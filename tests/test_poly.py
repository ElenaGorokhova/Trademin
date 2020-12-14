#!/usr/bin/env python

import os
import tempfile

import pytest

from .. import poly

EX_API_KEY = 'NaOW_Dp24BpexIR8A9qADvh3owYD98Ka'
EX_API_KEY_RANDOM = 'THISISNOTAVALIDKEYBUTITDOESNOTMATTER'


## load_config ##

def test_load_config__no_params():
    '''
    Running without passing parameters should raise an TypeError exception
    HINT: This is the standard way to test for (and handle) exceptions (errors)
          using standard built-in python funtions alone. It's a little
          bit more verbose, but also, more flexible and perhaps even, more
          readable.
    '''
    try:
        poly.load_config()
    except TypeError:
        assert True
    else:
        assert False


def test_load_config__valid_config():
    '''
    Running with a path known to actually point to a valid JSON file
    should return the contents of the JSON file (non-empty dictionary)
    HINT: pass in the path to `fixtures/polygon-example.json` file
    '''
    pass


def test_load_config__invalid_path():
    '''
    Running with an invalid path should raise an error
    HINT: This is another way to test for cases where python raises an exception
    '''
    invalid_path = 'XXX'
    pytest.raises(FileNotFoundError, poly.load_config, invalid_path)


def test_load_config__valid_non_json_file():
    '''
    Running with a path to contain a VALID, but NON-JSON should
    raise json.JSONDecodeError
    HINT: pass in a path to the fixtures/ValidButNotJSON.csv, for example
    '''
    pass


def test_load_config__empty_file():
    '''
    Running with a path to an existing, but EMPTY file should return an empty
    dictionary object.
    HINT: pass in a path to the fixtures/emptyfile.txt, for example
    '''
    pass


## load_api_key_from_path

def test_load_api_key_from_path__no_params():
    '''
    Running without passing parameters should raise an TypeError exception
    '''
    pass


def test_load_api_key_from_path__missing_api_key():
    '''
    Loading a valid JSON file that doesn't contain `api_key` key in the
    dictionary should return back None value, without raising any error
    '''
    pass


def test_load_api_key_from_path__valid_config():
    '''
    Loading a valid JSON file which contains `api_key` key should return
    back the value found under that api_key
    HINT: use polygon-example.json
    '''
    pass


## save_api_key_to_path

def test_save_api_key_to_path__new_valid_config_file_path():
    '''
    Passing a non-existing PATH should create that path, save the save the
    api_key value as valid JSON file and return True
    HINT: We want to work with TEMPORARY FILES and DIRECTORIES that we can
    clean up later etc without making a mess of our project space
    '''
    # create a temporary directory to save the json config in
    # HINT: using in this way (context manager) ensures that the
    # temporary directory is removed after the test is run
    with tempfile.TemporaryDirectory() as tdir:
        config_path = os.path.join(tdir, 'subdir/polygon.json')
        # try to create the new config with api_key defined
        poly.save_api_key_to_path(EX_API_KEY, config_path)
        # check that the config exists and contains api_key
        api_key = poly.load_api_key_from_path(config_path)
        assert api_key == EX_API_KEY

        # lets also check that we get the FileExistsError if we try to Write
        # over the existing file without overwrite set to True
        pytest.raises(FileExistsError,
                      poly.save_api_key_to_path,
                      EX_API_KEY,
                      config_path)

        # and finally check that are able to overwrite / update the api_key
        # value with overwrite == True
        poly.save_api_key_to_path(EX_API_KEY_RANDOM, config_path, True)
        # check that the config exists and contains api_key
        api_key = poly.load_api_key_from_path(config_path)
        assert api_key == EX_API_KEY_RANDOM



def test_save_api_key_to_path__null_value():
    '''
    Passing any null value should raise ValueError
    HINT: (None, '', "", 0, False, [], {}) are all registered as null
    '''
    pass


def test_save_api_key_to_path__non_json():
    '''
    Passing a PATH that doesn't point to a file with .json file extension
    should raise a RuntimeError.
    '''
    pass


def test_save_api_key_to_path__existing_path_no_overwrite():
    '''
    Passing a PATH to a valid existing JSON file, which also already
    defines 'api_key', without setting overwrite param, should raise
    FileExistsError.
    '''
    pass


def test_save_api_key_to_path__existing_path_overwrite_force():
    '''
    Passing a PATH to a valid existing JSON file, which also already
    defines 'api_key', while setting overwrite param to True, should
    update the contents of the api_key key value pair and save the File
    as expected.
    '''
    pass


def test_save_api_key_to_path__valid_config_api_key_not_defined():
    '''
    Passing a PATH to a valid existing JSON file,  which does not
    have api_key defined already, should return True and the
    path should now contain an updated config json which consists of
    the existing data values PLUS one additional api_key key and value pair.
    '''
    pass
