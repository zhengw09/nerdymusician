from flask import render_template, flash, redirect, session, request, url_for
from flask_login import current_user, login_user, logout_user
from app import app, forms, db
from app.models import User, Msg, Album, Image, ImageComment
from twilio.rest import Client
from twilio_config import twilio_config
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import hashlib
import os
from pyheif import read_heif
from PIL import Image as ImagePIL


IMAGE_FORMATS = ['png', 'jpg', 'bmp', 'gif', 'heic', 'jpeg']


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
			if user.id == 'mus':
				sms_notify('The musician logged in - ' + format_time_with_tz(datetime.now()))
		except:
			pass
		return redirect('/chat')
	return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
	try:
		if current_user.id == 'mus':
			sms_notify('The musician logged out - ' + format_time_with_tz(datetime.now()))
	except:
		pass
	logout_user()
	return redirect('/')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
	if not current_user.is_authenticated:
		return redirect('/login')
	form = forms.MsgForm()
	if form.validate_on_submit():
		db.session.add(Msg(current_user.id, form.msg.data))
		db.session.commit()
		flash('Message sent')
		return redirect(request.url)
	msgs = Msg.query.all()[::-1][:1000]
	unread_msgs = set()
	commit_flag = False
	for msg in msgs:
		if not msg.status:
			unread_msgs.add(msg.msg_id)
			if msg.from_user_id != current_user.id:
				commit_flag = True
				msg.status = True
		elif msg.status and msg.from_user_id != current_user.id:
			break
	if commit_flag:
		db.session.commit()
	return render_template('chat.html', form=form, msgs=msgs, format_time_with_tz=format_time_with_tz, unread_msgs=unread_msgs)


@app.route('/gallery')
def gallery():
	if not current_user.is_authenticated:
		return redirect('/login')
	albums = Album.query.all()
	return render_template('gallery.html', albums=albums)


@app.route('/album', methods=['GET', 'POST'])
def album():
	if not current_user.is_authenticated:
		return redirect('/')
	album_title = request.args.get('title')
	images = Image.query.filter_by(album=album_title).all()
	form = forms.ImageForm()
	if form.validate_on_submit():
		f = form.image.data
		caption = form.caption.data
		filename = secure_filename(f.filename)
		image_id = generate_image_id(album_title, filename)
		fmt = filename.split('.')[-1].lower()
		if fmt not in IMAGE_FORMATS:
			return redirect(request.url)
		if fmt == 'heic':
			fmt = 'jpg'
			hashed_file_name = '{}.{}'.format(image_id, fmt)
			heic_to_jpg(f, hashed_file_name)
		else:
			hashed_file_name = '{}.{}'.format(image_id, fmt)
			f.save(os.path.join(os.getcwd(), 'app/static/images', hashed_file_name))
		image = Image(image_id, fmt, album_title, caption=caption, uploaded_by=current_user.id)
		db.session.add(image)
		db.session.commit()
		return redirect(request.url)
	return render_template('album.html', images=images, form=form)


@app.route('/image', methods=['GET', 'POST'])
def image():
	if not current_user.is_authenticated:
		return redirect('/')
	image_id = request.args.get('image_id')
	image = Image.query.filter_by(image_id=image_id).first()
	if not image:
		return redirect('/gallery')
	album = Album.query.filter_by(title=image.album).first()
	curr_idx = album.images.index(image)
	prev_idx = curr_idx - 1 if curr_idx > 0 else len(album.images) - 1
	next_idx = curr_idx + 1 if curr_idx < len(album.images) - 1 else 0
	form = forms.MsgForm()
	if form.validate_on_submit():
		db.session.add(ImageComment(image_id, current_user.id, form.msg.data))
		db.session.commit()
		return redirect(request.url)
	return render_template('image.html', curr=image, prev=album.images[prev_idx], next=album.images[next_idx], comments=image.comments, format_time_with_tz=format_time_with_tz, form=form)


def sms_notify(notification):
	account_sid = twilio_config['sid']
	auth_token = twilio_config['token']
	client = Client(account_sid, auth_token)
	client.messages.create(body=notification, from_='+12564856537', to='+12066367689')


def format_time_with_tz(timestamp):
	return (timestamp - timedelta(hours=5)).strftime('%m/%d %H:%M')


def generate_image_id(album, filename):
	timestamp_str = datetime.now().strftime('%Y%m%d%H%M%S')
	return hashlib.md5((album + filename + timestamp_str).encode('utf-8')).hexdigest()


def heic_to_jpg(f, hashed_file_name):
	image_heic = read_heif(f)
	image_jpg = ImagePIL.frombytes(mode=image_heic.mode, size=image_heic.size, data=image_heic.data)
	image_jpg.save(os.path.join(os.getcwd(), 'app/static/images', hashed_file_name), format="jpeg")
