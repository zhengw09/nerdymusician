from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class MsgForm(FlaskForm):
    msg = TextAreaField('Msg', validators=[DataRequired()])
    send = SubmitField('Send')


class ImageForm(FlaskForm):
    image = FileField(validators=[FileRequired()])
    caption = TextAreaField('Caption')
    upload = SubmitField('Upload')
