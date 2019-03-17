from recommender import db

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imdb_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(), nullable=False)
    kind = db.Column(db.String(), nullable=False)
    url = db.Column(db.String(), nullable=False)
    vector = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"Movie({self.id}, '{self.title}', '{self.kind}')"

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    giantbomb_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(), nullable=False)
    url = db.Column(db.String(), nullable=False)
    vector = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"Game({self.id}, '{self.title}')"

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goodreads_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(), nullable=False)
    url = db.Column(db.String(), nullable=False)
    vector = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"Book({self.id}, '{self.title}')"