from flask import Flask, render_template, redirect, session, url_for, flash
from .. import db
from ..models import User
from . import main
from .forms import NameForm
@main.route('/')
def index():
	return render_template('index.html')
@main.route('/user/<username>')
def user(username):
	user=User.query.filter_by(username=username).first()
	if user is None:
		abort(404)
	return render_template('user.html',user=user)
