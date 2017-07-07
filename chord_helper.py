"""DB queries and helper functions for chord finder project"""

from model import User, Artist, ArtistSong, Song, Chord, SongChord, Favorite
from model import connect_to_db, db
import operator


def search_by_title(term):
    """Searches the db for songs using song title."""

    return Song.query.filter(Song.title.ilike('%{}%'.format(term))).all()


def search_by_artist(term):
    """Searches the db for songs using artist name."""

    results = []
    artist = Artist.query.filter(Artist.name.ilike('%{}%'.format(term))).all()

    for i in artist:
        results.extend(i.songs)

    return results


def find_songs_with_n_chords(n):
    """Seaches the db for songs with n chords.
    Returns list of song objects."""

    n_chord_songs = []
    all_songs = Song.query.options(db.joinedload('chords')).all()

    for song in all_songs:
        if len(song.chords) == n:
            n_chord_songs.append(song)

    return n_chord_songs


def find_songs_chords(chord_list):
    """Seaches the db for songs with specific chord names.
    Returns list of song objects."""

    chord_list.sort()

    chord_songs = []
    all_songs = Song.query.options(db.joinedload('chords')).all()

    for song in all_songs:

        songs_chords = []
        for chord in song.chords:
            songs_chords.append(chord.name)

        songs_chords.sort()

        if chord_list == songs_chords:
            chord_songs.append(song)

    return chord_songs


def query_chord_combos():
    """Searches the db for popular combinations of chords.
    Returns a dictionary with chord tuples as keys and counts as values."""

    chord_combos = {}

    all_songs = Song.query.options(db.joinedload('chords')).all()

    for song in all_songs:

        songs_chords = []
        for chord in song.chords:
            songs_chords.append(chord.name)

        songs_chords.sort()
        chord_key = tuple(songs_chords)
        chord_combos[chord_key] = chord_combos.get(chord_key, 0) + 1

    return chord_combos


def most_chord_combos():
    """Finds chord combinations used by the most songs.
    Returns a list of tuples."""

    chord_combos = query_chord_combos()
    sorted_chords = sorted(chord_combos.items(), key=operator.itemgetter(1), reverse=True)

    return sorted_chords[:5]


def shortest_chord_combos():
    """Finds chord combinations with the shortest amount of chords.
    Returns a list of tuples."""

    short_chords = []
    chord_combos = query_chord_combos()

    for key in chord_combos:
        if len(key) < 5:
            short_chords.append(key)

    short_chords.sort(key=len)
    return short_chords


def extract_song_info(song_objects):
    """ Takes a list of song objects and extracts song id, title, artists, and chords.
    Returns these as a list of tuples.
    Song info: (song_id, title, [artists], [chords]) """

    songs_list = []

    for song in song_objects:

        sid = song.song_id
        song_title = song.title

        artist_list = extract_artists(song)
        chord_list = extract_chords(song)

        songs_list.append((sid, song_title, artist_list, chord_list))

    return songs_list


def extract_artists(song_object):
    """Takes a song object and extracts artists as a list."""

    artist_list = []
    for artist in song_object.artists:
        artist_list.append(artist.name)

    return artist_list


def extract_chords(song_object):
    """Takes a song object and extracts chords as a list."""

    chord_list = []
    for chord in song_object.chords:
        chord_list.append(chord.name)

    return chord_list


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print "Connected to DB."