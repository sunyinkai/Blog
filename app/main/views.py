from flask import Flask, render_template, redirect, session, url_for, flash
from .. import db
from ..models import User
from . import main
from .forms import NameForm,EditProfileForm
from flask_login import login_required,current_user

@main.route('/')
def index():
	return render_template('index.html')
@main.route('/user/<username>')
def user(username):
	user=User.query.filter_by(username=username).first()
	if user is None:
		abort(404)
	return render_template('user.html',user=user)

@main.route('/edit-profile',methods=['GET','POST'])
@login_required
def edit_profile():
	form=EditProfileForm()
	if form.validate_on_submit():
		current_user.name=form.name.data
		current_user.location=form.location.data
		current_user.about_me=form.about_me.data
		db.session.add(current_user)
		db.session.commit()
		flash('Your infomation has been updated.')
		return redirect(url_for('.user',username=current_user.username))  #what's this logic
	form.name.data=current_user.name
	form.location.data=current_user.location
	form.about_me.data=current_user.about_me
	return render_template('edit_profile.html',form=form)
