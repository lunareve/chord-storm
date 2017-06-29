"""Utility file to seed favorites database from SongLens data in seed_data/"""

from sqlalchemy import func

from model import User, Artist, ArtistSong, Song, Chord, SongChord, Favorite

from model import connect_to_db, db
from server import app

import guitar_party_api as gp


def load_users():
    """Load users from u.user into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    email=email,
                    password=password)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_chords(song_list):
    """Load chords from Guitar Party API into database."""
    print "Chords"

    for item in song_list:
        chord_list = item['chords']

        for chord in chord_list:

            if Chord.query.filter_by(chord_code=chord['code']).first() == None:
                instrument = chord['instrument']

                chrd = Chord(chord_code=chord['code'],
                             name=chord['name'],
                             instrument=instrument['safe_name'])

                db.session.add(chrd)

        db.session.commit()


def load_artists(song_list):
    """Load artists from Guitar Party API into database."""
    print "Artists"

    for item in song_list:
        authors_list = item['authors']

        # Make a set of all authors in a song to remove duplicates
        # go through each item in the set to make Artist objects

        for author in authors_list:
            art_id = author['uri'].split('/')[-2]

            if Artist.query.filter_by(artist_id=art_id).first() == None:

                artist = Artist(artist_id=art_id,
                                name=author['name'])

                db.session.add(artist)
                db.session.commit()


def load_songs(song_list):
    """Load songs from Guitar Party API into database."""
    print "Songs"

    for item in song_list:

        song = Song(song_id=item['id'],
                    title=item['title'],
                    body=item['body'],
                    body_chords_html=item['body_chords_html'],
                    permalink=item['permalink'])

        db.session.add(song)

    db.session.commit()


def load_favorites():
    """Load favorites from u.data into database."""
    print "Favorites"

    Favorite.query.delete()

    for row in open("seed_data/u.data"):
        row = row.rstrip()
        user_id, song_id = row.split("\t")

        favorite = Favorite(user_id=user_id,
                            song_id=song_id)

        db.session.add(favorite)

    db.session.commit()


def load_songs_chords(song_list):
    """Load chords of a song from Guitar Party API into database."""
    print "Songs Chords"

    for item in song_list:
        chord_list = item['chords']

        for chord in chord_list:

            sc = SongChord(chord_code=chord['code'],
                           song_id=item['id'])

            db.session.add(sc)

    db.session.commit()


def load_artists_songs(song_list):
    """Load artists associated with a song from Guitar Party API into database."""
    print "Artists Songs"

    for item in song_list:
        authors_list = item['authors']

        for author in authors_list:
            artist_id = author['uri'].split('/')[-2]

            artsong = ArtistSong(artist_id=artist_id,
                                 song_id=item['id'])

            db.session.add(artsong)

    db.session.commit()


def seed_file():
    """Search songs from u.test with Guitar Party API
    to get back JSON to plug into load functions."""

    # Delete all rows in tables, so if we need to run this a second time,
    # we won't be trying to add duplicates
    SongChord.query.delete()
    ArtistSong.query.delete()
    Song.query.delete()
    Artist.query.delete()
    Chord.query.delete()

    for row in open("seed_data/u.test"):
        row = row.rstrip()
        song_list = gp.unwrap_songs(row)

        load_songs(song_list)
        load_artists(song_list)
        load_chords(song_list)
        load_songs_chords(song_list)
        load_artists_songs(song_list)


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import JSON data and seed to different tables
    seed_file()
    # load_users()
    # load_favorites()
    # set_val_user_id()
