from flask import Blueprint, render_template, flash, redirect
from utils import forms
from flask_login import current_user, login_user
from models.models import User


main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def index():
	return render_template('index.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect('/')
	form = forms.LoginForm()
	user = User.query.filter_by(username=form.username.data).first()
	if user is None or not user.check_password(form.password.data):
		flash('Invalid username or password')
		return redirect('/login')
	login_user(user)
	return redirect('/chat')

@main.route('/chat')
def chat():
	return render_template('chat.html')