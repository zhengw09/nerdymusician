from flask import render_template, flash, redirect
from flask_login import current_user, login_user
from app import app, forms
from app.models import User


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect('/')
	form = forms.LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(id=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect('/login')
		login_user(user)
		return redirect('/chat')
	return render_template('login.html', title='Login', form=form)


@app.route('/chat')
def chat():
	return render_template('chat.html')