from flask import Flask
from backend.routes import init_routes
import os

def create_app():
    app = Flask(__name__, template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), "../templates")))
    init_routes(app)
    return app
