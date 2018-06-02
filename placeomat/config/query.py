GMAPS_KEYS = {
    'search': 'query',
    'location': 'location',
}

# values are separated by comma if one value has mappings
# for multiple keys from search params to the expected params of the service
YELP_KEYS = {
    'search': 'location',
    'location': 'latitude,longitude',
}

KEY_MAPPING = {
    'google': GMAPS_KEYS,
    'yelp': YELP_KEYS}


def get_map(key_var):
    return KEY_MAPPING[key_var]
