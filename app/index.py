from dotenv import load_dotenv
from flask import Flask, jsonify, request

app = Flask(__name__)

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
        records = []
        records.append({
            "longitude": "0.0",
            "latitude": "0.0",
            "size" : "0",
            "hotness" : "0"
        })
        records.append({
            "longitude": "1.0",
            "latitude": "1.0",
            "size" : "1",
            "hotness" : "1"
        })
        return jsonify(records)
    except Exception as e:
        return jsonify(**{"error": e})


if __name__ == '__main__':
    load_dotenv()
    app.run(host='0.0.0.0', port=3000, debug=True)