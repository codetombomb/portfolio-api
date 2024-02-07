from flask import Flask
from flask_bcrypt import Bcrypt
import os

from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from oauthlib.oauth2 import WebApplicationClient
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False


db = SQLAlchemy()
ma = Marshmallow(app)

client = WebApplicationClient(os.environ.get("GOOGLE_CLIENT_ID"))

migrate = Migrate(app, db)
db.init_app(app)

bcrypt = Bcrypt(app)

CORS(app)

api = Api(app)