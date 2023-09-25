import os
from flask import Flask, jsonify

app = Flask(__name__)

# Get the secret from the environment variable
SECRET_KEY = os.environ.get("SECRET_KEY")

@app.route('/v1/api/helloworld', methods=['GET'])
def hello_world():
    if SECRET_KEY:
        return jsonify({"message": "Hello, World!", "secret": SECRET_KEY})
    else:
        return jsonify({"error": "Secret key not found."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
