from flask import request, make_response, session
from flask_restful import Resource

from models import Visitor, Admin

from config import app, api, db