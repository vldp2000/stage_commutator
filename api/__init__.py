from flask import Blueprint
api_bp = Blueprint('api_blueprint', __name__)
from . import api
api.initGPIO()