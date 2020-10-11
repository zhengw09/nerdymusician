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


class Album(db.Model):
    title = db.Column(db.String(64), primary_key=True)
    created_timestamp = db.Column(db.DateTime, index=True)
    created_by = db.Column(db.String(64))
    last_updated_timestamp = db.Column(db.DateTime, index=True)
    last_updated_by = db.Column(db.String(64))
    images = db.relationship('Image', backref=db.backref('folder', lazy=True))

    def __init__(self, title, created_by='admin', last_updated_by='admin'):
        self.title = title
        self.created_timestamp = datetime.now()
        self.last_updated_timestamp = self.created_timestamp
        self.created_by = created_by
        self.last_updated_by = last_updated_by

    def __repr__(self):
        return '<Album {}>'.format(self.title)


class Image(db.Model):
    image_id = db.Column(db.String(64), primary_key=True)
    format = db.Column(db.String(64))
    album = db.Column(db.String(64), db.ForeignKey('album.title'))
    caption = db.Column(db.Text)
    uploaded_timestamp = db.Column(db.DateTime, index=True)
    uploaded_by = db.Column(db.String(64))
    comments = db.relationship('ImageComment', backref=db.backref('comment_of', lazy=True))

    def __init__(self, image_id, fmt, album, caption="", uploaded_by='admin'):
        self.image_id = image_id
        self.format = fmt
        self.album = album
        self.caption = caption
        self.uploaded_timestamp = datetime.now()
        self.uploaded_by = uploaded_by

    def __repr__(self):
        return '<Image {}.{} in {}>'.format(self.image_id, self.format, self.album)

    def set_caption(self, caption):
        self.caption = caption


class ImageComment(db.Model):
    comment_id = db.Column(db.String(64), primary_key=True)
    image_id = db.Column(db.String(64), db.ForeignKey('image.image_id'))
    from_user_id = db.Column(db.String(64))
    text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __init__(self, image_id, from_user_id, text):
        now = datetime.now()
        self.comment_id = now.strftime("%Y%m%d, %H:%M:%S.%f")[:-3]
        self.image_id = image_id
        self.from_user_id = from_user_id
        self.text = text
        self.timestamp = now

    def __repr__(self):
        return '<Comment for {} by {} at {}>'.format(self.image_id, self.from_user_id, self.comment_id)
