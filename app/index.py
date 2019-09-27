from dotenv import load_dotenv
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/post_something', methods=['POST'])
def api_post_something():
    try:
        json_data = request.get_json()
        return jsonify(**{"hello": json_data['hello']})
    except Exception as e:
        return jsonify(**{"error": e})


@app.route('/api/get_something', methods=['GET'])
def api_get_something():
    return jsonify(**{"hello": "world"})


if __name__ == '__main__':
    load_dotenv()
    app.run(host='0.0.0.0', port=3000, debug=True)