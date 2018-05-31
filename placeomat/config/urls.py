URLS = {'google': 'https://maps.googleapis.com/maps/api/place/textsearch/json',
        'yelp': 'https://api.yelp.com/v3/businesses/search'}

MORE_DETAILS = {'google': 'https://maps.googleapis.com/maps/api/place/details/json',
                'yelp': 'URL'}
# assuming textsearch for Google Places API as it allows for keyword as well as
# location (latlong)
# Google Places nearbysearch only takes latlong

def get_url(url_name):
    return URLS[url_name]
