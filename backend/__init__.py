from flask import Flask
from backend.routes import init_routes
import os

def create_app():
    app = Flask(__name__,  static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), "../static")), template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), "../templates")))
    app.config['SECRET_KEY'] = 'your_secret_key'  # Use a unique secret key
    init_routes(app)
    return app
