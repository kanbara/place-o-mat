from placeomat.config import urls
from placeomat.providers import provider
from placeomat.gmaps import status as gstatus

from requests.compat import urlencode, urlparse



class Provider(provider.Provider):
    def __init__(self):
        self.name = 'Google Maps'
        super(Provider, self).__init__(key_var='google')

    def extra_query_params(self):
        data = {'key': self.api_key}
        return data

    def build_query_headers(self):
        return None

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
        if code not in gstatus.VALID_CODES:
            result = {
                'status': 'INVALID',  # make this a constant
                'reason': 'Got response code %d' % code
            }
        res = self.response.json()
        status = res['status']
        if status != gstatus.OK:
            # ideally we would do some metric/tracing here to find out why
            result = {
                'status': 'INVALID',
                'reason': gstatus.REASONS[status]
            }
        else:

            items = res['results']
            results = []
            for item in items:
                data = {
                    'ID': item['id'],
                    'Provider': self.name,
                    'Name': item['name'],
                    'Location': (item['geometry']['location']['lat'],
                                 item['geometry']['location']['lng']),
                    'Address': item['formatted_address'],
                    'More Details': self.build_details_url(item['place_id'])
                }
                results += [data]

            result = {
                'status': 'VALID',
                'results': results
            }

        return result
