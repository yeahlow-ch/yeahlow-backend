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

        dataAccess.add(
            float(json_data['latitude']), 
            float(json_data['longitude']), 
            int(json_data['vote'])
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


@app.route('/api/db', methods=['DELETE'])
def api_delete_database():
    try:
        VOTES.deleteAll()
        EVENTS.deleteAll()
        return jsonify({}), 200
    except Exception as e:
        return jsonify(**{"error": e})


@app.route('/api/db', methods=['POST'])
def api_init_database():
    try:
        VOTES.addFakeData()
        EVENTS.addFakeData()
        return jsonify({}), 200
    except Exception as e:
        return jsonify(**{"error": e})


if __name__ == '__main__':
    load_dotenv()
    app.run(host='0.0.0.0', port=port, debug=True)