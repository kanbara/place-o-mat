import logging

from placeomat.providers import provider
from placeomat.yelp import status as ystatus
from placeomat.yelp import validation


class Provider(provider.Provider):
    def __init__(self):
        self.name = 'Yelp'
        super(Provider, self).__init__(key_var='yelp')

    def extra_query_params(self, **kwargs):
        return {}

    def validate_params(self, params):
        if 'open_now' in params.keys():
            # API requires a boolean value
            params['open_now'] = True

        radius = params.get('radius', None)
        if radius:
            # max radius is 40km
            # https://www.yelp.com/developers/documentation/v3/business_search
            if int(radius) > validation.MAX_RADIUS:
                raise provider.ValidationException(
                    'radius was %d, must be less than %d' % (
                        int(radius), validation.MAX_RADIUS))

        # require either location or lat/long
        lat_long = params.get('latitude', None) and \
            params.get('longitude', None)

        location = params.get('location', None)

        if not (lat_long or location):
            raise provider.ValidationException(
                'Must supply latitude and longitude, or location')

        return params

    def build_query_headers(self):
        headers = {'Authorization': 'Bearer %s' % self.api_key}
        return headers

    def response(self):
        """
        Once a query has been made, response can be called to parse the request
        response, and return the appropriately formatted dictionary.

        :return: response dictionary
        :rtype: dict
        """

        code = self._response.status_code

        if code not in ystatus.VALID_CODES:
            return self._make_response(
                provider.Status.INVALID,
                reason='Got response code %d' % code)

        res = self._response.json()
        items = res.get('businesses', [])

        if not items:
            return self._make_response(
                provider.Status.VALID,
                reason="No results found")

        results = []
        for item in items:
            # TODO: could make this bit extensible
            data = {
                'ID': item['id'],
                'Provider': self.name,
                'Name': item['name'],
                'Description': ', '.join(
                    [c['title'] for c in item['categories']]),
                'Location': (item['coordinates']['latitude'],
                             item['coordinates']['longitude']),
                'Address': ' '.join(item['location']['display_address']),
                'More Details': item['url']
            }
            results += [data]

        return self._make_response(
            provider.Status.VALID,
            results=results)
