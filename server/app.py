from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Episode, Guest, Appearance


app  = Flask(__name__)

app = config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lateshow.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
     return '''
    <h1> Welcome to the Late Show API!</h1>
    <p>The API is up and running.</p>
    <h2>Available Endpoints:</h2>
    <ul>
        <li><strong>GET</strong> /episodes - Get all episodes</li>
        <li><strong>GET</strong> /episodes/:id - Get specific episode</li>
        <li><strong>DELETE</strong> /episodes/:id - Delete episode</li>
        <li><strong>GET</strong> /guests - Get all guests</li>
        <li><strong>POST</strong> /appearances - Create new appearance</li>
    </ul>
    <p>Visit the endpoints above or use the Postman collection to test the API.</p>
    '''

@app.route('/episodes', nethods=['GET'])
def get_episodes():
     
     
    episodes = Episode.query.all()
    episodes_dict = [episode.to_dict(only=('id', 'date', 'number')) for episode in episodes]

    return jsonify(episodes_dict), 200


@app.route('/episodes/<int:id>', method=['GET'])
def get_episode(id):
     
    episode = Episode.query.filter(Episode.id == id).first()
    if episode is None:
        return jsonify(
            {"error": "Episode not found"}
        ), 404
    
    episode_dict = episode.to_dict(only=('id', 'date', 'number', 'appearances'))

    if 'appearances' in episode_dict:
        formatted_appearances = []

        for appearance in episode_dict['appearances']:
            app_obj = Appearance.query.get(appearance['id'])

            formatted_app = {
                'id': appearance['id'],
                'rating': appearance['rating'],
                'episode_id': appearance['episode_id'],
                'guest_id': appearance['guest_id'],

                'guest':app_obj.guest.to_dict(only=('id', 'name', 'occupation'))
            }
            formatted_appearances.append(formatted_app)

        episode_dict['appearances'] = formatted_appearances
    
    return jsonify(episode_dict), 200



     
    

