import csv
import os
from app import app
from models import db, Episode, Guest, Appearance

def seed_database():
    """Seed the database with sample data from CSV files."""
    with app.app_context():
        Appearance.query.delete()
        Episode.query.delete()
        Guest.query.delete()
        
        episodes_csv = os.path.join(os.path.dirname(__file__), 'episodes.csv')
        episodes = []
        if os.path.exists(episodes_csv):
            with open(episodes_csv, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    episodes.append(row)
        
        guests_csv = os.path.join(os.path.dirname(__file__), 'guests.csv')
        guests = []
        if os.path.exists(guests_csv):
            with open(guests_csv, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    guests.append(row)
        
        appearances_csv = os.path.join(os.path.dirname(__file__), 'appearances.csv')
        appearances_data = []
        if os.path.exists(appearances_csv):
            with open(appearances_csv, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    appearances_data.append(row)
        
        episode_map = {}
        for ep in episodes:
            episode = Episode(
                id=int(ep['id']),
                date=ep['date'],
                number=int(ep['number'])
            )
            db.session.add(episode)
            episode_map[episode.id] = episode
        
        guest_map = {}
        for guest in guests:
            guest_obj = Guest(
                id=int(guest['id']),
                name=guest['name'],
                occupation=guest['occupation']
            )
            db.session.add(guest_obj)
            guest_map[guest_obj.id] = guest_obj
        
        for app_data in appearances_data:
            appearance = Appearance(
                rating=int(app_data['rating']),
                episode_id=int(app_data['episode_id']),
                guest_id=int(app_data['guest_id'])
            )
            db.session.add(appearance)
        
        db.session.commit()
        print(f"Database seeded with {len(episodes)} episodes, {len(guests)} guests, and {len(appearances_data)} appearances.")

if __name__ == '__main__':
    seed_database()

