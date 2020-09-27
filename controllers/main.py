from flask import Blueprint, render_template, flash, redirect
from utils import forms, password


main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def index():
	return render_template('index.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
	form = forms.LoginForm()
	if form.validate_on_submit() and password.validate(form.data):
		flash('Logging in')
		return redirect('/chat')
	return render_template('login.html', title='Login', form=form)


@main.route('/chat')
def chat():
	return render_template('chat.html')