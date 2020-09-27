from flask import Flask
import controllers
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

# Register the controllers
app.register_blueprint(controllers.main)
app.secret_key = 'thiswillbeouryear'
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
