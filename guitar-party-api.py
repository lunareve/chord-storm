import requests

# URL Only returns a single URI
# If need to search multiple songs, need to remove the '/' at the end of the URL

VERSION = '0.1'
URL = 'http://api.guitarparty.com/v2/%(resource)s/'
QUERY = 'http://api.guitarparty.com/v2/%(resource)s'
API_KEY = 'e7829b22224fa082e9eaa3a865ba5a18df9f062d'

def request(resource, **params):
    """Returns JSON from a single URI (song, artist, or chord)."""
    options = {
        'headers': {
            'Guitarparty-Api-Key': API_KEY,
        },
    }
    options.update(params)
    r = requests.get(URL % {'resource': resource}, **options)
    return r.json()


def query(resource, **params):
    """Returns a JSON list from a query."""
    options = {
        'headers': {
            'Guitarparty-Api-Key': API_KEY,
        },
    }
    options.update(params)
    r = requests.get(QUERY % {'resource': resource}, **options)
    return r.json()


def format_search(search_term):
    """Replace any spaces with '+'."""

    pass


def query_songs(search_term):
    """Get a list of songs. Search term must have '+' instead of spaces."""
    songs = query('songs/?query={}'.format(search_term))

    pass


over_the_rainbow = request('songs/365')
chords_dict = over_the_rainbow['chords']
chord_names = []

for chord in chords_dict:
    chord_names.append(chord['name'])
