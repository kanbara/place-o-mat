OK = 'OK'
ZERO_RESULTS = 'ZERO_RESULTS'
OVER_LIMIT = 'OVER_QUERY_LIMIT'
REQUEST_DENIED = 'REQUEST_DENIED'
INVALID_REQUEST = 'INVALID_REQUEST'
UNKNOWN_ERROR = 'UNKNOWN_ERROR'
NOT_FOUND = 'NOT_FOUND'

VALID_CODES = [200]

# here, we can eventually flesh out some of these by for example
# checking which paramters are required by the API, and returning that
#
# also, we likely should not be exposing if our API key is over the limit
REASONS = {
    OK: 'No errors occurred',
    ZERO_RESULTS: 'No results found for search parameters',
    OVER_LIMIT: 'Query Limit Exceeded',
    REQUEST_DENIED: 'Missing required parameters',
    INVALID_REQUEST: 'Missing required parameters',
    UNKNOWN_ERROR: 'Unknown error; please try again',
    NOT_FOUND: 'No results for Place ID',
}
