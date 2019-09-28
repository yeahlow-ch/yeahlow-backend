import os
from dataAccess import Votes

from dotenv import load_dotenv
from flask import Flask, jsonify, request

import firebase_admin
from firebase_admin import credentials, firestore

port = int(os.getenv('PORT', 3000))

app = Flask(__name__)

cred = credentials.Certificate("./firebase_key.json")
firebase_admin.initialize_app(cred)
dataAccess = Votes(firestore.client().collection('votes'))

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


@app.route('/api/db', methods=['DELETE'])
def api_delete_database():
    try:
        dataAccess.deleteAll()
        return jsonify({}), 200
    except Exception as e:
        return jsonify(**{"error": e})


@app.route('/api/db', methods=['POST'])
def api_init_database():
    try:
        dataAccess.addFakeData()
        return jsonify({}), 200
    except Exception as e:
        return jsonify(**{"error": e})


if __name__ == '__main__':
    load_dotenv()
    app.run(host='0.0.0.0', port=port, debug=True)