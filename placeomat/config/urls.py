URLS = {'google': 'https://maps.googleapis.com/maps/api/place/textsearch/json',
        'yelp': 'https://api.yelp.com/v3/businesses/search'}

MORE_DETAILS = {'google': 'https://maps.googleapis.com/maps/api/place/details/json',
                'yelp': None}
# assuming Text Search for Google Places API as it allows for keyword as well
# as location (latlong), Google Places Nearby Search only takes latlong,
# and not a query string like "cafes in sydney"

def get_url(provider):
    """
    Get the URL to query given a provider name

    :param provider str: provider to query
    :return: URL of service
    :rtype: string
    """

    return URLS[provider]

def get_more_details_url(provider):
    """
    Get the URL to query for more details given a provider name

    :param provider str: provider to query
    :return: URL of service
    :rtype: string
    """

    return MORE_DETAILS[provider]
