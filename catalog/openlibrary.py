import requests

BASE_URL = 'https://openlibrary.org/api/books?'

_jscmd = 'data'
_format = 'json'

def _normalize_bibkey(bibkey):
    k = 'ISBN' if bibkey[0].lower().startswith('isbn') else bibkey[0].upper()
    return ':'.join([k, bibkey[1]])
    
def _normalize_bibkeys(bibkeys):
    return ','.join(_normalize_bibkey(bibkey) for bibkey in bibkeys)


def search_by_isbn(isbn):
    return search(('ISBN', isbn))


def search(bibkey):
    try:
        return search_bulk([bibkey])[_normalize_bibkey(bibkey)]
    except KeyError:
        return {}

def search_bulk(bibkeys):
    params = {
        'bibkeys': _normalize_bibkeys(bibkeys),
        'format': 'json',
        'jscmd': 'data',
    }

    resp = requests.get(BASE_URL, params=params, timeout=5)
    return resp.json()
