"""Utility file to seed favorites database from SongLens data in seed_data/"""

from sqlalchemy import func

from model import User, Artist, ArtistSong, Song, Chord, ChordList, Favorite

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


def load_chords():
    """Load chords from file into database."""
    print "Chords"

    Chord.query.delete()

        chord = Chord(chord_code=chord_code,
                      instrument=instrument,
                      image_url=image_url)

        db.session.add(chord)

    db.session.commit()


def load_artists():
    """Load artists from Guitar Party API into database."""
    print "Artists"

    Artist.query.delete()

        artist = Artist(artist_id=artist_id,
                        name=name)

        db.session.add(artist)

    db.session.commit()


def load_songs():
    """Load songs from Guitar Party API into database."""
    print "Songs"

    Song.query.delete()

        song = Song(song_id=song_id,
                    title=title,
                    body=body,
                    body_chords_html=body_chords_html,
                    permalink=permalink)

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


def load_chord_list():
    """Load chord list from u.data into database."""
    print "Chord List"

    ChordList.query.delete()

    for row in open("seed_data/u.data"):
        row = row.rstrip()
        chord_code, song_id = row.split("\t")

        cl = ChordList(chord_code=chord_code,
                       song_id=song_id)

        db.session.add(cl)

    db.session.commit()


def load_artists_songs():
    """Load artists songs from u.data into database."""
    print "Artists Songs"

    ArtistSong.query.delete()

    for row in open("seed_data/u.data"):
        row = row.rstrip()
        artist_id, song_id = row.split("\t")

        favorite = Favorite(artist_id=artist_id,
                            song_id=song_id)

        db.session.add(favorite)

    db.session.commit()


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

    # Import different types of data
    # load_users()
    load_songs()
    # load_favorites()
    # set_val_user_id()
