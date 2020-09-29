from flask import render_template, flash, redirect, session
from flask_login import current_user, login_user, logout_user
from app import app, forms, db
from app.models import User, Msg
from twilio.rest import Client


@app.before_request
def modify_session():
	session.modified = True


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
		if user.id == 'musician':
			sms_notify('The musician logged in')
		return redirect('/chat')
	return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect('/')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
	if current_user.is_authenticated:
		form = forms.MsgForm()
		if form.validate_on_submit():
			db.session.add(Msg(current_user.id, form.msg.data))
			db.session.commit()
			flash('Message sent')
			form.msg.data = None
		msgs = Msg.query.all()[::-1][:100]
		return render_template('chat.html', form=form, msgs=msgs)
	return redirect('/')


@app.route('/gallery')
def gallery():
	if current_user.is_authenticated:
		return render_template('gallery.html')
	return redirect('/')


def sms_notify(notification):
	account_sid = 'AC2acc1674726676f3c5ddbdef1e9cfaea'
	auth_token = '6221b27375e8dd084b6f3551f19dd062'
	client = Client(account_sid, auth_token)
	client.messages.create(body=notification, from_='+12564856537', to='+17342390706')
