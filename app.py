from flask import Flask, request, jsonify
from models import db, Episode, Guest, Appearance
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    return app

app = create_app()

@app.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([episode.to_dict() for episode in episodes])

@app.route('/episodes/<int:episode_id>', methods=['GET'])
def get_episode(episode_id):
    episode = Episode.query.get(episode_id)
    
    if not episode:
        return jsonify({"error": "Episode not found"}), 404
    
    return jsonify(episode.to_dict(include_appearances=True))

@app.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    return jsonify([guest.to_dict() for guest in guests])

@app.route('/appearances', methods=['POST'])
def create_appearance():
    data = request.get_json()
    
    if not data:
        return jsonify({"errors": ["No input data provided"]}), 400
    
    # Check required fields
    errors = []
    for field in ['rating', 'episode_id', 'guest_id']:
        if field not in data or data[field] is None:
            errors.append(f"{field} is required")
    
    if 'rating' in data and data['rating'] is not None:
        if data['rating'] < 1 or data['rating'] > 5:
            errors.append("rating must be between 1 and 5")
    
    # Validate foreign keys exist
    if 'episode_id' in data and not Episode.query.get(data['episode_id']):
        errors.append("episode not found")
    
    if 'guest_id' in data and not Guest.query.get(data['guest_id']):
        errors.append("guest not found")
    
    if errors:
        return jsonify({"errors": errors}), 400
    
    try:
        appearance = Appearance(
            rating=data['rating'],
            episode_id=data['episode_id'],
            guest_id=data['guest_id']
        )
        
        db.session.add(appearance)
        db.session.commit()
        
        return jsonify(appearance.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": ["Failed to create appearance"]}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(port=5000)

