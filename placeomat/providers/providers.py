from placeomat.providers import gmaps
from placeomat.providers import yelp
import json

PROVIDERS = {
    'gmaps': gmaps.Provider,
    'yelp': yelp.Provider,
}


def query_all(query):
    results = []
    for provider in PROVIDERS.values():
        p = provider()
        p.query(query)
        res = p.results()
        if res['status'] == 'VALID':
            results.append(res['results'])

    return results
