import logging

from placeomat.config import urls
from placeomat.providers import provider
from placeomat.gmaps import status as gstatus
from placeomat.gmaps import validation

import requests
from requests.compat import urlencode, urlparse


class Provider(provider.Provider):
    def __init__(self):
        self.name = 'Google Maps'
        super(Provider, self).__init__(key_var='google')

    def extra_query_params(self):
        data = {'key': self.api_key}
        return data

    def validate_params(self, params):
        radius = params.get('radius', None)
        if radius:
            # max radius is 50km
            # https://developers.google.com/places/web-service/search
            if int(radius) > validation.MAX_RADIUS:
                raise provider.ValidationException(
                    'radius was %d, must be less than %d' % (
                        int(radius), validation.MAX_RADIUS))

        return params

    def build_query_headers(self):
        return None

    def place_details(self, place_id):
        """
        Gets the extra details about a place from the Places API

        :param str place_id: Places API place_id
        :return: Places API Response
        """
        url = urls.MORE_DETAILS['google']
        params = {'placeid': place_id, 'key': self.api_key}
        logging.debug('Making request to %s with %s',
                      url, params)
        response = requests.get(url, params=params)

        code = response.status_code
        if code not in gstatus.VALID_CODES:
            return self._make_response(
                provider.Status.INVALID,
                reason='Got response code %d' % code)

        res = response.json()
        status_code = res['status']

        if status_code != gstatus.OK:
            return self._make_response(
                provider.Status.INVALID,
                reason=gstatus.REASONS[status_code])
        else:
            return self._make_response(
                provider.Status.VALID,
                results={
                    'url': res['result']['url'],
                    'website': res['result'].get('website', 'None'),
                })

    def response(self):
        """
        Once a query has been made, response can be called to parse the request
        response, and return the appropriately formatted dictionary.

        :return: response dictionary
        :rtype: dict
        """
        code = self._response.status_code

        # so far, we only handle 200. Not sure what else the API
        # can/will return
        if code not in gstatus.VALID_CODES:
            return self._make_response(
                provider.Status.INVALID,
                reason='Got response code %d' % code)

        res = self._response.json()
        status_code = res['status']

        if status_code != gstatus.OK:

            # a response of zero results is "VALID" but we want to tell
            # the user that the service was fine, and that there were simply
            # no results found for the given query.
            if status_code == gstatus.ZERO_RESULTS:
                return self._make_response(
                    provider.Status.VALID,
                    reason=gstatus.REASONS[status_code])

            # ideally we would do some metric/tracing here to find out why
            # but for now we can just return that something went wrong
            return self._make_response(
                provider.Status.INVALID,
                reason=gstatus.REASONS[status_code])
        else:  # success case
            results = []
            items = res['results']
            for item in items:
                # XXX: not sure what the description would be here
                # Places API does not offer the description of a place
                # through its API (e.g. "Asian Fusion Restaurant")
                # so instead, we use the types, which are nouns that
                # tell a bit about a place
                #
                # return the place_id here, so users can then ask
                # for more details, as well
               
                # TODO: handle this better in terms of parsing and
                # error response
                more_details_url = 'Could not get more details'
                details = self.place_details(item['place_id'])
                if details['status'] is provider.Status.VALID:
                    more_details_url = details['results']

                data = {
                    'ID': item['place_id'],
                    'Provider': self.name,
                    'Name': item['name'],
                    'Description': ', '.join(item['types']),
                    'Location': (item['geometry']['location']['lat'],
                                 item['geometry']['location']['lng']),
                    'Address': item['formatted_address'],
                    'More Details': more_details_url,
                }
                results += [data]

            return self._make_response(
                provider.Status.VALID,
                results=results)
