from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Episode(db.Model):
    """Episode model representing a late show episode."""
    __tablename__ = 'episodes'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    
    appearances = db.relationship('Appearance', backref='episode_ref', 
                                   cascade='all, delete-orphan', lazy=True)
    
    guests = association_proxy('appearances', 'guest')
    
    def to_dict(self, include_appearances=False):
        """Serialize episode to dictionary."""
        data = {
            'id': self.id,
            'date': self.date,
            'number': self.number
        }
        
        if include_appearances:
            data['appearances'] = [appearance.to_dict() for appearance in self.appearances]
        
        return data
    
    def __repr__(self):
        return f'<Episode {self.id}: {self.date}>'


class Guest(db.Model):
    """Guest model representing a guest on the late show."""
    __tablename__ = 'guests'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    occupation = db.Column(db.String(100), nullable=False)
    
    appearances = db.relationship('Appearance', backref='guest_ref', 
                                   cascade='all, delete-orphan', lazy=True)
    
    episodes = association_proxy('appearances', 'episode')
    
    def to_dict(self):
        """Serialize guest to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'occupation': self.occupation
        }
    
    def __repr__(self):
        return f'<Guest {self.id}: {self.name}>'


class Appearance(db.Model):
    """Appearance model representing a guest's appearance on an episode."""
    __tablename__ = 'appearances'
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id', ondelete='CASCADE'), 
                          nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id', ondelete='CASCADE'), 
                        nullable=False)
    
    @validates('rating')
    def validate_rating(self, key, rating):
        """Validate that rating is between 1 and 5."""
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        return rating
    
    def to_dict(self, include_nested=True):
        """Serialize appearance to dictionary."""
        data = {
            'id': self.id,
            'rating': self.rating,
            'guest_id': self.guest_id,
            'episode_id': self.episode_id
        }
        
        if include_nested:
            data['episode'] = self.episode_ref.to_dict()
            data['guest'] = self.guest_ref.to_dict()
        
        return data
    
    def __repr__(self):
        return f'<Appearance {self.id}: Guest {self.guest_id} on Episode {self.episode_id}>'

