from flask import Blueprint

bp = Blueprint('main', __name__)

# must import routes here
from app.main import routes

