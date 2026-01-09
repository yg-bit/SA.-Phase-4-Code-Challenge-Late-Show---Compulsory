import csv
import os
from app import app
from models import db, Episode, Guest, Appearance

def seed_database():
    with app.app_context():
        # Clear existing data
        Appearance.query.delete()
        Episode.query.delete()
        Guest.query.delete()
        
        # Load CSV data
        base_dir = os.path.dirname(__file__)
        
        episodes = []
        episodes_file = os.path.join(base_dir, 'episodes.csv')
        if os.path.exists(episodes_file):
            with open(episodes_file, 'r') as f:
                episodes = list(csv.DictReader(f))
        
        guests = []
        guests_file = os.path.join(base_dir, 'guests.csv')
        if os.path.exists(guests_file):
            with open(guests_file, 'r') as f:
                guests = list(csv.DictReader(f))
        
        appearances_data = []
        appearances_file = os.path.join(base_dir, 'appearances.csv')
        if os.path.exists(appearances_file):
            with open(appearances_file, 'r') as f:
                appearances_data = list(csv.DictReader(f))
        
        # Add episodes
        for ep in episodes:
            try:
                episode = Episode(
                    id=int(ep['id']),
                    date=ep['date'],
                    number=int(ep['number'])
                )
                db.session.add(episode)
            except (ValueError, KeyError) as e:
                print(f"Skipping invalid episode data: {ep}")
        
        # Add guests
        for guest_data in guests:
            try:
                guest = Guest(
                    id=int(guest_data['id']),
                    name=guest_data['name'],
                    occupation=guest_data['occupation']
                )
                db.session.add(guest)
            except (ValueError, KeyError) as e:
                print(f"Skipping invalid guest data: {guest_data}")
        
        # Add appearances
        for app_data in appearances_data:
            try:
                appearance = Appearance(
                    rating=int(app_data['rating']),
                    episode_id=int(app_data['episode_id']),
                    guest_id=int(app_data['guest_id'])
                )
                db.session.add(appearance)
            except (ValueError, KeyError) as e:
                print(f"Skipping invalid appearance data: {app_data}")
        
        db.session.commit()
        print(f"Seeded {len(episodes)} episodes, {len(guests)} guests, {len(appearances_data)} appearances")

if __name__ == '__main__':
    seed_database()

