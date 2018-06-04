import logging

from placeomat.providers import gmaps
from placeomat.providers import yelp
from placeomat.providers.provider import Status, ValidationException

# register each provider here, in order to get nice client side validation
# as well as the ability to query each provider
PROVIDERS = {
    'google': gmaps.Provider,
    'yelp': yelp.Provider,
}


def parse_response(response):
    """
    Parses an internal response from a provider query. Gets the
    status codes, results list and reason for failure, if any.

    :param dict response: response from query
    :return: HTTP status code, result list, and reason
    :rtype: tuple

    """
    # a result should always have a status
    status = response['status']

    # a result _may_ have a results or a reason
    result = response.get('results', [])
    reason = response.get('reason', None)

    return status, result, reason


def _get_response_message(code=200, reason=None):
    """
    Convenience method to format the response to a query. This method should
    be used when there are no results to display to the user, or there
    was an error in the provider's request. The result will be easily
    jsonified to present well to consumers of the API.

    :param int code: HTTP Status Code, optional, defaults to 200 OK
    :param str reason: Reason for error, optional.

    :return: dict with reason, HTTP Status Code
    :rtype: tuple
    """
    return {'reason': reason}, code


# TODO: combine query and query_all to reduce duplicate logic for
# return codes
def query(provider_str, query):
    """
    The heart of the API. This method instantiates providers and
    calls their query methods to fetch data with the given query parameters.

    It can operate on all providers simultaneously, or only on one.

    :param str provider_str: the provider to query, or 'all'. The provider will be validated against available providers
    :param dict query: the query to send to the provider

    :return: result of the query or reason for failure, and HTTP Status Code
    :rtype: tuple
    """
    if provider_str == 'all':
        try:
            res = query_all(query)
        except ValidationException as ve:
            return _get_response_message(400, reason=str(ve))

        return res, 200
    else:
        provider = _validate_provider(provider_str)
        if not provider:
            reason = '%s not a valid provider, choices are %s' % (
                provider_str,
                ', '.join(PROVIDERS.keys()))
            return _get_response_message(400, reason=reason)

        try:
            provider.query(query)
        except ValidationException as ve:
            return _get_response_message(400, reason=str(ve))

        status, result, reason = parse_response(provider.response())
        logging.debug("Got status %s (%s), %d results",
                      status, reason, len(result))
        if status == Status.VALID:
            if len(result):
                return result, 200
            else:  # no results found!
                logging.info("Provider %s got empty results", provider.name)
                return _get_response_message(reason=reason)
        else:
            logging.info("Provider %s got bad request: %s",
                         provider, reason)
            return _get_response_message(400, reason=reason)


def _validate_provider(provider):
    """
    Method to ensure the provider passed in exists. If it exists, the provider will be instantiated.

    :param str provider: provider to check
    :return: Provider
    :rtype: Provider
    """
    if PROVIDERS.get(provider, None):
        return PROVIDERS[provider]()
    else:
        return None


def query_all(query):
    """
    Convenience method to query all providers. This method can build a list of results for multiple providers.

    :param dict query: query params to send to each provider
    :return: result of the query or reason for failure, and HTTP Status Code
    :rtype: tuple

    """
    results = []
    statuses = []
    for provider in PROVIDERS.values():
        p = provider()
        p.query(query)
        status, result, reason = parse_response(p.response())
        statuses.append(status)

        if status == Status.VALID:
            results += result
        elif status == Status.INVALID:
            logging.info("Provider %s got invalid status: %s",
                         p.name, reason)
            return _get_response_message(400, reason=reason)

    if len(results):
        return results, 200
    else:
        if all([s == Status.VALID for s in statuses]):
            logging.info("Provider %s got empty results", p.name)
            return _get_response_message(reason=reason)
        else:
            logging.info("Provider %s got bad request: %s",
                         p.name, reason)
            return _get_response_message(400, reason=reason)
