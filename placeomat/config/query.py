GMAPS_KEYS = {
    'query': 'query',
    'location': 'location',
    'radius': 'radius',
    'open': 'opennow',
}

# values are separated by comma if one value has mappings
# for multiple keys from search params to the expected params of the service
YELP_KEYS = {
    'query': 'term',
    'location': 'latitude,longitude',
    'radius': 'radius',
    'open': 'open_now',
}

KEY_MAPPING = {
    'google': GMAPS_KEYS,
    'yelp': YELP_KEYS
}


def get_map(provider):
    """
    Get the map for the given provider

    :param str provider: provider to get map for
    :return: mapping dictionary
    :rtype: dict
    """
    return KEY_MAPPING[provider]
