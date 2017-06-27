"""Models and database functions for Favorites project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of chord finder website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email =%s>" % (self.user_id,
                                                self.email)


class Artist(db.Model):
    """Artist of chord finder website"""

    __tablename__ = "artists"

    artist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Artist artist_id=%s name=%s>" % (self.artist_id,
                                              self.name)


class Song(db.Model):
    """Song of chord finder website."""

    __tablename__ = "songs"

    song_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    artist_id = db.Column(db.ForeignKey('artists.artist_id', nullable=False))
    body = db.Column(db.Blob, nullable=True)
    body_chords_html = db.Column(db.Blob, nullable=True)
    permalink = db.Column(db.String(200), nullable=True)

    # Define relationship to artist
    artist = db.relationship("Artist",
                             backref=db.backref("songs",
                                                order_by=song_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Song song_id=%s title=%s>" % (self.song_id,
                                               self.title)


class Chord(db.Model):
    """Chord of chord finder website"""

    __tablename__ = "chords"

    code = db.Column(db.String(10), primary_key=True)
    instrument = db.Column(db.String(20), nullable=True)
    image_url = db.Column(db.String(150), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Chord code=%s>" % (self.code)


class Chord_List(db.Model):
    """Chord list of chord finder website."""

    __tablename__ = "chord_list"

    chord_list_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.song_id'), nullable=False)
    chord = db.Column(db.String, db.ForeignKey('chords.code'), nullable=False)

    # Define relationship to chord
    chord = db.relationship("Chord",
                            backref=db.backref("chord_list",
                                               order_by=chord_list_id))

    # Define relationship to song
    song = db.relationship("Song",
                           backref=db.backref("chord_list",
                                              order_by=chord_list_id))

    def __repr__(self):
        """Provide helpful representation of Favorite when printed."""

        s = "<Chord List chord_list_id=%s song_id=%s chord=%s>"
        return s % (self.chord_list_id, self.song_id, self.chord)


class Favorite(db.Model):
    """Favorite of chord finder website."""

    __tablename__ = "favorites"

    favorite_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.song_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("favorites",
                                              order_by=favorite_id))

    # Define relationship to song
    song = db.relationship("Song",
                            backref=db.backref("favorites",
                                               order_by=favorite_id))

    def __repr__(self):
        """Provide helpful representation of Favorite when printed."""

        s = "<Favorite favorite_id=%s song_id=%s user_id=%s>"
        return s % (self.favorite_id, self.song_id, self.user_id)



##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///chordfinder'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
