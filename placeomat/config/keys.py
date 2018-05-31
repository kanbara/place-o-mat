import os
import logging

KEYS = {'google': 'GMAPS_KEY',
        'yelp': 'YELP_KEY'}


class KeyNotFound(Exception):
    pass


def get_key(key_name):
    key_var = KEYS[key_name]
    try:
        key = os.environ[key_var]
    except KeyError as ke:
        raise Exception('Could not find %s in environment' % key_var) from ke

    return key
