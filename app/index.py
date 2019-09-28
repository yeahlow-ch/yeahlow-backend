import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request

import firebase_admin
from firebase_admin import credentials, firestore

port = int(os.getenv('PORT', 3000))

app = Flask(__name__)
cred = credentials.Certificate("./firebase_key.json")
firebase_admin.initialize_app(cred)
VOTES = firestore.client().collection('votes')

@app.route('/api/votes', methods=['POST'])
def api_post_votes():
    try:
        json_data = request.get_json()
        print(json_data)
        return jsonify({}), 201
    except Exception as e:
        return jsonify(**{"error": e})


@app.route('/api/votes', methods=['GET'])
def api_get_votes():
    try:
        results = []
        for row in VOTES.stream():
            doc = row.to_dict()
            results.append({
                "longitude" : doc['location'].longitude,
                "latitude" : doc['location'].latitude,
                "size" : 1,
                "hotness" : 1
            })
        return jsonify(results)
    except Exception as e:
        return jsonify(**{"error": e})


if __name__ == '__main__':
    load_dotenv()
    app.run(host='0.0.0.0', port=port, debug=True)