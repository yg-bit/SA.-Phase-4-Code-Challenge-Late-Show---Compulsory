from flask import Flask, request, jsonify
from models import db, Episode, Guest, Appearance
from config import Config

def create_app(config_class=Config):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    return app

app = create_app()

@app.route('/episodes', methods=['GET'])
def get_episodes():
    """Return all episodes as a list of dictionaries."""
    episodes = Episode.query.all()
    return jsonify([episode.to_dict() for episode in episodes])

@app.route('/episodes/<int:episode_id>', methods=['GET'])
def get_episode(episode_id):
    """Return a single episode by ID with its appearances."""
    episode = Episode.query.get(episode_id)
    
    if not episode:
        return jsonify({"error": "Episode not found"}), 404
    
    return jsonify(episode.to_dict(include_appearances=True))

@app.route('/guests', methods=['GET'])
def get_guests():
    """Return all guests as a list of dictionaries."""
    guests = Guest.query.all()
    return jsonify([guest.to_dict() for guest in guests])

@app.route('/appearances', methods=['POST'])
def create_appearance():
    """Create a new appearance associated with an episode and guest."""
    data = request.get_json()
    
    if not data:
        return jsonify({"errors": ["No input data provided"]}), 400
    
    rating = data.get('rating')
    episode_id = data.get('episode_id')
    guest_id = data.get('guest_id')
    
    errors = []
    if rating is None:
        errors.append("rating is required")
    if episode_id is None:
        errors.append("episode_id is required")
    if guest_id is None:
        errors.append("guest_id is required")
    
    if rating is not None and (rating < 1 or rating > 5):
        errors.append("rating must be between 1 and 5")
    
    episode = Episode.query.get(episode_id)
    if not episode:
        errors.append("episode not found")
    
    guest = Guest.query.get(guest_id)
    if not guest:
        errors.append("guest not found")
    
    if errors:
        return jsonify({"errors": errors}), 400
    
    appearance = Appearance(
        rating=rating,
        episode_id=episode_id,
        guest_id=guest_id
    )
    
    db.session.add(appearance)
    db.session.commit()
    
    return jsonify(appearance.to_dict()), 201

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)

