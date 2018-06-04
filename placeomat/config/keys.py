import os
import logging

# location of our API Keys in the environment
KEYS = {'google': 'GMAPS_KEY',
        'yelp': 'YELP_KEY'}


class KeyNotFound(Exception):
    pass


def get_key(key_name):
    """ Get the key for the provider from the system environment """
    key_var = KEYS[key_name]
    try:
        key = os.environ[key_var]
    except KeyError as ke:
        raise KeyNotFound('Could not find %s in environment' % key_var) from ke

    return key
