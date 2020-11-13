from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'ThisWillBeOurYear'
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
app.permanent_session_lifetime = timedelta(seconds=30)

from app import routes, models
