from app.models import Pizza, create_db
from flask import Blueprint
routes = Blueprint('routes', __name__)

from .connection import *