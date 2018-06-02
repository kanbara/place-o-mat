from placeomat.config import urls
from placeomat.providers import provider
from placeomat.yelp import status as ystatus

from requests.compat import urlencode, urlparse


class Provider(provider.Provider):
    def __init__(self):
        self.name = 'Yelp'
        super(Provider, self).__init__(key_var='yelp')

    def extra_query_params(self, **kwargs):
        # must return {} here
        return {}

    def build_query_headers(self):
        headers = {'Authorization': 'Bearer %s' % self.api_key}
        return headers

    def build_details_url(self, place_id):
        base_url = urls.MORE_DETAILS['google']
        params = urlencode({
            'placeid': place_id,
            'key': self.api_key,
        })

        add_token = '&' if urlparse(base_url).query else '?'
        more_details_url = base_url + add_token + params

        return more_details_url

    def results(self):
        code = self.response.status_code
        if code not in ystatus.VALID_CODES:
            result = {
                'status': 'INVALID',  # make this a constant
                'reason': 'Got response code %d' % code
            }
        res = self.response.json()
        items = res.get('businesses', [])
        results = []
        for item in items:
            data = {
                'ID': item['id'],
                'Provider': self.name,
                'Name': item['name'],
                'Location': (item['coordinates']['latitude'],
                             item['coordinates']['longitude']),
                'Address': ' '.join(item['location']['display_address']),
                'More Details': item['url']
            }
            results += [data]

        result = {
            'status': 'VALID',
            'results': results
        }

        return result
