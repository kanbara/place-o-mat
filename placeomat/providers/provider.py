import logging
import requests
from placeomat.config import keys, urls, query
from abc import ABCMeta, abstractmethod


# abstract class for providers
class Provider(object):
    __metaclass__ = ABCMeta

    def __init__(self, key_var):
        self.api_url = urls.get_url(key_var)
        self.api_key = keys.get_key(key_var)
        self.map = query.get_map(key_var)

    @abstractmethod
    def build_query_headers():
        pass

    @abstractmethod
    def extra_query_params(self):
        pass

    def parse_query_string(self, query_string):
        args = {}
        kv_pairs = query_string.split('&')
        for kv in kv_pairs:
            kv = kv.split('=')
            if len(kv) == 2:
                k, v = kv
                args[k] = v
            else:
                continue

        return args

    def build_query_params(self, **kwargs):
        args_mapped = self.map_args(**kwargs)
        print(args_mapped)
        return args_mapped

    def map_args(self, **kwargs):
        mapped_args = {}
        default_args = {}

        for k, v in kwargs.items():
            mapped_key = self.map.get(k, None)

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
                    values_to_map = [v]

                for i, key in enumerate(keys_to_map):
                    logging.debug('Mapping key "%s" to "%s"', k, key)

                    mapped_args[key] = values_to_map[i].strip()
            else:
                default_args[k] = v

        logging.debug("Generated mapped args: %s", mapped_args)
        logging.debug("Remaining args: %s", default_args)

        args = {**mapped_args, **default_args}
        return args

    def query(self, query_string):
        query_args = self.parse_query_string(query_string)
        logging.debug('Making query with %s in provider %s',
                      query_args,
                      self.name)

        base_params = self.build_query_params(**query_args)
        extra_params = self.extra_query_params()

        # python 3.4 magic to combine two dicts
        # XXX: will merge values if duplicate keys exist
        params = {**base_params, **extra_params}
        headers = self.build_query_headers()
        res = requests.get(self.api_url, params=params, headers=headers)
        self.response = res

    @abstractmethod
    def results(self):
        # format as
        # ID
        # Provider
        # Name
        # Description
        # Location (latlong)
        # Address
        # URI
        pass
