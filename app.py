from flask import Flask, send_file
from routes import register_routes

app = Flask(__name__, static_folder="build/static")

register_routes(app)

if __name__ == "__main__":
    app.run(port=3001, debug=True)