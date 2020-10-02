from flask import render_template, flash, redirect, session, request
from flask_login import current_user, login_user, logout_user
from app import app, forms, db
from app.models import User, Msg, Album, Image
from twilio.rest import Client
from twilio_config import twilio_config
from datetime import datetime, timedelta


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
		try:
			if user.id == 'musician':
				sms_notify('The musician logged in - ' + format_time_with_tz(datetime.now()))
		except:
			pass
		return redirect('/chat')
	return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
	try:
		if current_user.id == 'musician':
			sms_notify('The musician logged out - ' + format_time_with_tz(datetime.now()))
	except:
		pass
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
		return render_template('chat.html', form=form, msgs=msgs, format_time_with_tz=format_time_with_tz)
	return redirect('/')


@app.route('/gallery')
def gallery():
	if current_user.is_authenticated:
		albums = Album.query.all()
		return render_template('gallery.html', albums=albums)
	return redirect('/')


@app.route('/album')
def album():
	if current_user.is_authenticated:
		title = request.args.get('title')
		images = Image.query.filter_by(album=title).all()
		if not images:
			return redirect('/gallery')
		current_idx = int(request.args.get('idx', '0'))
		next_idx = current_idx + 1 if current_idx < len(images) - 1 else 0
		return render_template('images.html', current=images[current_idx], next=images[next_idx], next_idx=next_idx)
	return redirect('/')


def sms_notify(notification):
	account_sid = twilio_config['sid']
	auth_token = twilio_config['token']
	client = Client(account_sid, auth_token)
	client.messages.create(body=notification, from_='+12564856537', to='+17342390706')


def format_time_with_tz(timestamp):
	return (timestamp - timedelta(hours=4)).strftime('%m/%d %H:%M')
