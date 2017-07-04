"""DB queries and helper functions for chord finder project"""

from model import User, Artist, ArtistSong, Song, Chord, SongChord, Favorite
from model import connect_to_db, db


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