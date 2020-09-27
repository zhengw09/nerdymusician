from flask import Flask
import controllers

app = Flask(__name__)

# Register the controllers
app.register_blueprint(controllers.main)
app.secret_key = 'thiswillbeouryear'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
