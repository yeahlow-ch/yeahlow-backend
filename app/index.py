import os
from dataAccess import DataAccess

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS


port = int(os.getenv('PORT', 3000))

app = Flask(__name__)
CORS(app)

dataAccess = DataAccess()

@app.route('/api/votes', methods=['POST'])
def api_post_votes():
    try:
        json_data = request.get_json()

        dataAccess.addVote(
            float(json_data['latitude']), 
            float(json_data['longitude']), 
            int(json_data['vote']),
            "Foundation Technopark Zurich"
        )

        return jsonify({}), 201
    except Exception as e:
        return jsonify(**{"error": e})


@app.route('/api/votes', methods=['GET'])
def api_get_votes():
    try:
        return jsonify(dataAccess.getHotspots()), 200
    except Exception as e:
        return jsonify(**{"error": e})


@app.route('/api/events', methods=['GET'])
def api_get_events():
    try:
        return jsonify(dataAccess.getEvents()), 200
    except Exception as e:
        return jsonify(**{"error": e})


@app.route('/api/events/surprise', methods=['GET'])
def api_get_suprise_event():
    try:
        longitude = float(request.args.get('longitude'))
        latitude = float(request.args.get('latitude'))
        range = float(request.args.get('range'))

        return jsonify(dataAccess.getSurpriseEvent(longitude, latitude, range)), 200
    except Exception as e:
        return jsonify(**{"error": e})


@app.route('/api/db/events', methods=['DELETE'])
def api_delete_events():
    try:
        dataAccess.deleteAllEvents()
        return jsonify({}), 200
    except Exception as e:
        return jsonify(**{"error": e})


@app.route('/api/db/events', methods=['POST'])
def api_init_events():
    try:
        dataAccess.addFakeEvents()
        return jsonify({}), 200
    except Exception as e:
        return jsonify(**{"error": e})


@app.route('/api/db/votes', methods=['DELETE'])
def api_delete_votes():
    try:
        dataAccess.deleteAllVotes()
        return jsonify({}), 200
    except Exception as e:
        return jsonify(**{"error": e})


@app.route('/api/db/votes', methods=['POST'])
def api_init_votes():
    try:
        dataAccess.addFakeVotes()
        return jsonify({}), 200
    except Exception as e:
        return jsonify(**{"error": e})


if __name__ == '__main__':
    load_dotenv()
    app.run(host='0.0.0.0', port=port, debug=True)