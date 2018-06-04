import logging
import requests
from enum import Enum
from abc import ABCMeta, abstractmethod

from placeomat.config import keys, urls, query


class Status(Enum):
    """ Simple enum for cleaner status handling (e.g. without magic strings)"""
    INVALID = 1
    VALID = 2


class ValidationException(Exception):
    pass


# abstract class for providers
class Provider(object):
    """
    The Provider class is the superclass of all providers. It provides an
    __init__ which looks up the URL and API key needed for queries, as well
    as the map from the external API parameters to each specific API.

    The mapping lookup is done so that a service provider can be implemented
    without a lot of method definitions; it is more lightweight, but also
    less robust. For this implementation, provider simplicity was taken into
    consideration. A more complex approach may be needed in the future.

    This class is an Abstract Base Class.
    """
    __metaclass__ = ABCMeta

    def __init__(self, key_var):
        self.api_url = urls.get_url(key_var)
        self.api_key = keys.get_key(key_var)
        self.map = query.get_map(key_var)

    @abstractmethod
    def build_query_headers():
        """
        Implement this method to add headers to the query request,
        such as an API Key.
        """
        pass

    @abstractmethod
    def extra_query_params(self):
        """
        Implement this method to add parameters internal to the provider query
        such as an API Key.
        """
        pass

    @abstractmethod
    def validate_params(self, params):
        """
        Validate and cleanup parameters, such as adding required truthy values
        to fields that got mapped, or checking value ranges for certain keys``
        """
        pass

    # TODO: this and parse_response should be made into a class for better
    # code quality.
    def _make_response(self, status, results=[], reason=None):
        """
        Convenience method to make an internal response which can be
        used to return the query response from the provider.

        :param status int: HTTP Status Code
        :param results list: results from query
        :param reason str: reason why request failed, if applicable

        :return: response dictionary
        :rtype: dict
        """

        res = {}
        res['status'] = status
        res['results'] = results
        res['reason'] = reason

        return res

    def build_query_params(self, **kwargs):
        """
        Build query parameters from the query string. So far, this method
        only handles taking parameters from the external API and mapping
        them to internal provider parameters.

        :param kwargs dict: Parameters of query
        :return: Mapped parameters specific to the provider request
        :rtype: dict
        """
        args_mapped = self.map_args(**kwargs)
        return args_mapped

    def map_args(self, **kwargs):
        """
        Maps parameters based on the provider specific parameter names.
        Also can handle splitting multiple parameters.

        For example, a provider can map search(text)->query(text), which
        would mean the search parameter becomes query, and the value
        remains unchanged.

        A provider can map location(lat,long)->lat(lat),long(long), which
        maps a single key, location, into two keys lat, and long _and_
        separates their values.

        Additionally, a provider can map key(val1,val2)->newkey(val1,val2)

        :param kwargs dict: input parameters to map
        :return: mapped parameters plus all parameters that were not
        mapped which stay as the default key(val) that was passed in.
        :rtype: dict
        """

        # args that get mapped
        mapped_args = {}
        # args that stay the same (fail to map)
        default_args = {}

        for k, v in kwargs.items():
            mapped_key = self.map.get(k, None)

            # everything _not_ covered here remains unmapped as default_args
            if mapped_key:
                # check if we have a one-to-many for keys
                keys_to_map = mapped_key.split(',')

                # only split values if we also successfully split keys
                # e.g. we want to support single keys with multiple values
                # like location = 'lat,long'
                #
                # but also lat,long = 'latval,longval' to turn into
                # lat=latval, long=longval
                if len(keys_to_map) > 1:
                    values_to_map = v.split(',')
                else:
                    # note the [], which allows the below logic to work
                    # for single values as well as multiple ones
                    values_to_map = [v]

                for i, key in enumerate(keys_to_map):
                    logging.debug('Mapping key "%s" to "%s"', k, key)
                    mapped_args[key] = values_to_map[i].strip()
            else:
                default_args[k] = v

        logging.debug("Generated mapped args: %s", mapped_args)
        logging.debug("Remaining args: %s", default_args)

        # combine the dicts together (python3 syntax)
        args = {**mapped_args, **default_args}
        return args

    def query(self, query_args):
        """
        Make a query! Providers do not need to implement this,
        it can be extended as needed to support more providers.

        The query method takes parameters, builds the correct dictionary
        that the request can take, as well as extra headers needed.

        The request gets made, and the result is stored in the providers'
        response object.

        :param query_args dict: query parameters
        :return: None
        :rtype: None
        """

        logging.debug('Making query with %s in provider %s',
                      query_args,
                      self.name)

        base_params = self.build_query_params(**query_args)
        extra_params = self.extra_query_params()

        # python 3.4 magic to combine two dicts
        # will merge values if duplicate keys exist
        params = {**base_params, **extra_params}

        params = self.validate_params(params)
        headers = self.build_query_headers()

        self._response = requests.get(
            self.api_url, params=params, headers=headers)

    @abstractmethod
    def response(self):
        """
        The response method in a provider will take the self.response
        and format a dictionary with the fields:

        ID, Provider, Name, Description, Location, Address, Details URI

        :return: a list of places, each place being a dictionary
        :rtype: list
        """
        # ID
        # Provider
        # Name
        # Description
        # Location (latlong)
        # Address
        # URI
        pass
