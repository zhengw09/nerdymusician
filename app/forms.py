from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

__all__ = ['LoginForm', 'MsgForm']


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class MsgForm(FlaskForm):
    msg = TextAreaField('Msg', validators=[DataRequired()])
    send = SubmitField('Send')
