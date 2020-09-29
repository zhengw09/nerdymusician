from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.String(64), primary_key=True)
    password_hash = db.Column(db.String(128))
    msgs = db.relationship('Msg', backref=db.backref('owner', lazy=True))

    def __init__(self, id, password):
        self.id = id
        self.set_password(password)

    def __repr__(self):
        return '<User {}>'.format(self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(id)


class Msg(db.Model):
    msg_id = db.Column(db.String(64), primary_key=True)
    from_user_id = db.Column(db.Text, db.ForeignKey('user.id'))
    text = db.Column(db.String(2400))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    status = db.Column(db.Boolean)

    def __init__(self, from_user_id, text):
        now = datetime.now()
        self.msg_id = now.strftime("%Y%m%d, %H:%M:%S.%f")[:-3]
        self.from_user_id = from_user_id
        self.text = text
        self.timestamp = now
        self.status = False

    def __repr__(self):
        return '<Msg by {} at {}>'.format(self.from_user_id, self.msg_id)
