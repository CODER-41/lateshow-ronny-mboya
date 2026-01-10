from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention= {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
})

db = SQLAlchemy(metadata=metadata)

class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'

    serialize_rules = ('-appearances.episode',)

    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(db.String)

    number = db.Column(db.Integer)

    appearances = db.relationship('Appearance', back_populates='episodes', cascade='all, delete-orpahn')

    guests = association_proxy('appearances', 'guest')

    def __repr__(self):
        return f'<Episode {self.id}: {self.number}>'
    


class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'

    serialize_rules = ('-appearances.guest',)

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String)

    occupation = db.Column(db.String)

    appearances = db.relationship('Appearance', back_populates='guest', cascade='all, delete-orphan')

    episodes = association_proxy('appearances', 'episode')

    def __repr__(self):
        return f'<Guest {self.id}: {self.name}>'
    