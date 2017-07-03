"""DB queries and helper functions for chord finder project"""

from model import User, Artist, ArtistSong, Song, Chord, SongChord, Favorite
from model import connect_to_db, db
from server import app


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


if __name__ == "__main__":
    connect_to_db(app)