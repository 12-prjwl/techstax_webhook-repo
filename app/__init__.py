from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # MongoDB setup
    client = MongoClient(app.config["MONGO_URI"])
    app.mongo = client["your_database_name"]  # Replace with the name of your database

    # Enable CORS
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Register routes
    from .routes import main
    app.register_blueprint(main)

    return app
