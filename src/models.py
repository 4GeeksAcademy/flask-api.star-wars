from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    favorites = db.relationship('Favorite', backref='user', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    favorites = db.relationship('Favorite', backref='people', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    favorites = db.relationship('Favorite', backref='planet', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.email if self.user else None,
            "people": self.people.name if self.people else None,
            "planet": self.planet.name if self.planet else None
        }
