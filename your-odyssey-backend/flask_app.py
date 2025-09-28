import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Import the agent library (keeps AI logic separate from webserver)
from trip_planner.agent import travel_agent
from trip_planner.auth0 import requires_auth
from trip_planner import db as tp_db
import json
from dataclasses import asdict

app = Flask(__name__, static_folder='trip_planner/templates', template_folder='trip_planner/templates')
CORS(app)


@app.route('/')
def index():
    # If an index.html exists in trip_planner/templates, serve it; otherwise simple message
    try:
        return send_from_directory(app.template_folder, 'index.html')
    except Exception:
        return "YourOdyssey Flask backend is running. Use /generate_itinerary or /ask_question.", 200


@app.route('/generate_itinerary', methods=['POST'])
def generate_itinerary():
    data = request.get_json(force=True) or {}
    destination = (data.get('destination') or '').strip()
    departure_location = (data.get('departure_location') or '').strip()
    try:
        duration = int(data.get('duration', 3))
    except Exception:
        duration = 3
    preferences = (data.get('preferences') or '').strip()
    budget = (data.get('budget') or 'moderate').strip()

    if not destination:
        return jsonify({'error': 'Destination is required'}), 400

    if duration < 1 or duration > 14:
        return jsonify({'error': 'Duration must be between 1 and 14 days'}), 400

    try:
        full_itinerary = travel_agent.generate_itinerary(destination, duration, preferences, budget, departure_location)

        itinerary_dict = {
            'destination': full_itinerary.destination,
            'duration': full_itinerary.duration,
            'outbound_transport': asdict(full_itinerary.outbound_transport),
            'return_transport': asdict(full_itinerary.return_transport),
            'days': [asdict(day) for day in full_itinerary.days],
            'destination_info': full_itinerary.destination_info,
            'practical_info': full_itinerary.practical_info
        }

        return jsonify({'success': True, 'itinerary': itinerary_dict})

    except Exception as e:
        return jsonify({'error': f'Failed to generate itinerary: {str(e)}'}), 500


@app.route('/ask_question', methods=['POST'])
def ask_question():
    data = request.get_json(force=True) or {}
    question = (data.get('question') or '').strip()

    if not question:
        return jsonify({'error': 'Question is required'}), 400

    try:
        answer = travel_agent.ask_question(question)
        return jsonify({'success': True, 'answer': answer})
    except Exception as e:
        return jsonify({'error': f'Failed to get answer: {str(e)}'}), 500


@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'model': 'gemini-2.0-flash-exp'})


@app.route('/saved_trips', methods=['POST'])
@requires_auth
def save_trip():
    data = request.get_json(force=True) or {}
    itinerary = data.get('itinerary')
    if not itinerary:
        return jsonify({'error': 'Itinerary data required'}), 400

    # user identifier from token
    user_sub = getattr(request, 'auth_payload', {}).get('sub')
    if not user_sub:
        return jsonify({'error': 'Unable to determine user from token'}), 400

    try:
        rowid = tp_db.save_itinerary(user_sub, json.dumps(itinerary))
        return jsonify({'success': True, 'id': rowid}), 201
    except Exception as e:
        return jsonify({'error': f'Failed to save itinerary: {e}'}), 500


@app.route('/saved_trips', methods=['GET'])
@requires_auth
def list_trips():
    user_sub = getattr(request, 'auth_payload', {}).get('sub')
    if not user_sub:
        return jsonify({'error': 'Unable to determine user from token'}), 400

    try:
        items = tp_db.list_itineraries(user_sub)
        # parse itinerary JSON
        for it in items:
            try:
                it['itinerary'] = json.loads(it['itinerary_json'])
                del it['itinerary_json']
            except Exception:
                it['itinerary'] = None

        return jsonify({'success': True, 'items': items})
    except Exception as e:
        return jsonify({'error': f'Failed to list itineraries: {e}'}), 500


@app.route('/me', methods=['GET'])
@requires_auth
def me():
    payload = getattr(request, 'auth_payload', {})
    # Return a safe subset of claims to the frontend
    safe = {
        'sub': payload.get('sub'),
        'email': payload.get('email'),
        'email_verified': payload.get('email_verified'),
        'name': payload.get('name'),
        'picture': payload.get('picture'),
        'iss': payload.get('iss')
    }
    return jsonify({'success': True, 'user': safe})


@app.route('/profile', methods=['GET'])
@requires_auth
def get_profile():
    user_sub = getattr(request, 'auth_payload', {}).get('sub')
    if not user_sub:
        return jsonify({'error': 'Unable to determine user from token'}), 400
    try:
        profile = tp_db.get_profile(user_sub)
        if not profile:
            return jsonify({'success': True, 'profile': {'id': user_sub, 'bio': ''}})
        return jsonify({'success': True, 'profile': profile})
    except Exception as e:
        return jsonify({'error': f'Failed to get profile: {e}'}), 500


@app.route('/profile', methods=['POST'])
@requires_auth
def save_profile():
    user_sub = getattr(request, 'auth_payload', {}).get('sub')
    if not user_sub:
        return jsonify({'error': 'Unable to determine user from token'}), 400
    data = request.get_json(force=True) or {}
    bio = (data.get('bio') or '').strip()
    try:
        tp_db.save_profile(user_sub, bio)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': f'Failed to save profile: {e}'}), 500


@app.route('/follows', methods=['GET'])
@requires_auth
def list_follows():
    user_sub = getattr(request, 'auth_payload', {}).get('sub')
    if not user_sub:
        return jsonify({'error': 'Unable to determine user from token'}), 400

    try:
        items = tp_db.list_follows(user_sub)
        # return basic shape
        return jsonify({'success': True, 'items': items})
    except Exception as e:
        return jsonify({'error': f'Failed to list follows: {e}'}), 500


@app.route('/users/<user_id>', methods=['GET'])
@requires_auth
def get_user(user_id):
    # Return cached profile info if present, otherwise minimal info
    try:
        profile = tp_db.get_followed_profile(user_id)
        if profile:
            return jsonify({'success': True, 'user': profile})
        # fallback: return only id
        return jsonify({'success': True, 'user': {'id': user_id}})
    except Exception as e:
        return jsonify({'error': f'Failed to fetch user: {e}'}), 500


@app.route('/users/<user_id>/saved_trips', methods=['GET'])
@requires_auth
def list_user_saved_trips(user_id):
    try:
        items = tp_db.list_itineraries(user_id)
        for it in items:
            try:
                it['itinerary'] = json.loads(it['itinerary_json'])
                del it['itinerary_json']
            except Exception:
                it['itinerary'] = None
        return jsonify({'success': True, 'items': items})
    except Exception as e:
        return jsonify({'error': f'Failed to list user saved trips: {e}'}), 500


def _is_local_request():
    # allow dev-only unauthenticated helpers only from localhost
    addr = request.remote_addr
    return addr in ('127.0.0.1', '::1')


@app.route('/dev/follows', methods=['GET'])
def dev_list_follows():
    if not _is_local_request():
        return jsonify({'error': 'Not allowed'}), 403
    try:
        items = tp_db.list_follows('auth0|me')
        return jsonify({'success': True, 'items': items})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/dev/users/<user_id>', methods=['GET'])
def dev_get_user(user_id):
    if not _is_local_request():
        return jsonify({'error': 'Not allowed'}), 403
    try:
        profile = tp_db.get_followed_profile(user_id)
        if profile:
            return jsonify({'success': True, 'user': profile})
        return jsonify({'success': True, 'user': {'id': user_id}})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/dev/users/<user_id>/saved_trips', methods=['GET'])
def dev_list_user_saved_trips(user_id):
    if not _is_local_request():
        return jsonify({'error': 'Not allowed'}), 403
    try:
        items = tp_db.list_itineraries(user_id)
        for it in items:
            try:
                it['itinerary'] = json.loads(it['itinerary_json'])
                del it['itinerary_json']
            except Exception:
                it['itinerary'] = None
        return jsonify({'success': True, 'items': items})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', '5000'))
    host = os.getenv('HOST', '0.0.0.0')
    print(f"Starting YourOdyssey Flask app on {host}:{port}")
    # Ensure DB exists
    try:
        tp_db.init_db()
    except Exception as e:
        print(f"Failed to initialize DB: {e}")

    app.run(debug=True, host=host, port=port)
