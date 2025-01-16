from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from config import Config

def create_app():
    my_flask_app = Flask(__name__)
    my_flask_app.config.from_object(Config)

    # MongoDB setup
    client = MongoClient(my_flask_app.config["MONGO_URI"])
    my_flask_app.mongo = client["your_database_name"]  # Replace with the name of your database

    # CORS
    CORS(my_flask_app, resources={r"/*": {"origins": "*"}})

    from .routes import main
    my_flask_app.register_blueprint(main)

    return my_flask_app
