import unittest
from unittest.mock import patch, Mock

from placeomat.providers import provider


class TestProviderMap(unittest.TestCase):
    @patch('placeomat.providers.provider.urls')
    @patch('placeomat.providers.provider.keys')
    @patch('placeomat.providers.provider.query')
    def setUp(self, mock_urls, mock_keys, mock_query):

        self.provider = provider.Provider(key_var='mocked')
        self.provider.name = 'TestProvider'
        self.provider.map = {'one-to-one': 'singlekey',
                             'one-to-many': 'key1,key2',
                             'one-to-many2': 'key1, key2'}

        self.single_value = 'singlevalue'
        self.multiple_values = 'value1,value2'
        self.multiple_with_space = 'value1, value2'
        self.multiple_mapped = {'key1': 'value1',
                                'key2': 'value2'}

    def test_map_single(self):
        """ Test single key mapped """
        key = 'one-to-one'
        res = self.provider.map_args(**{key: self.single_value})
        exp = {self.provider.map[key]: self.single_value}

        self.assertEqual(exp, res)

    def test_map_single_multiple_values(self):
        """ Test single key mapped with multiple values """
        key = 'one-to-one'
        res = self.provider.map_args(**{key: self.multiple_values})
        exp = {self.provider.map[key]: self.multiple_values}

        self.assertEqual(exp, res)

    def test_no_map_single(self):
        """ Test single key not mapped """
        bad_key = 'testfoobar'
        some_val = 'banana'
        res = self.provider.map_args(**{bad_key: some_val})
        exp = {bad_key: some_val}

        self.assertEqual(exp, res)

    def test_map_mult(self):
        """ Test multiple keys with no space """
        key = 'one-to-many'
        res = self.provider.map_args(**{key: self.multiple_values})
        exp = self.multiple_mapped

        self.assertEqual(exp, res)

    def test_map_mult_space(self):
        """ Test multiple keys with spaces """
        key = 'one-to-many'
        res = self.provider.map_args(**{key: self.multiple_with_space})
        exp = self.multiple_mapped

        self.assertEqual(exp, res)
