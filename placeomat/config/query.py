GMAPS_KEYS = {
    'search': 'query',
}

YELP_KEYS = {
    'search': 'location',
}

KEY_MAPPING = {
    'google': GMAPS_KEYS,
    'yelp': YELP_KEYS}


def get_map(key_var):
    return KEY_MAPPING[key_var]
