from flask import Flask, render_template, redirect, session, url_for, flash
from .. import db
from ..models import User
from . import main
from .forms import NameForm
@main.route('/')
def index():
	return render_template('index.html')

@main.route('/login',methods=['GET','POST'])
def login():
	name=None
	form=NameForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.name.data).first()
		if user is None :
			user = User(username = form.name.data)
			db.session.add(user)
			db.session.commit()
			session['known']=False
		else:
			session['known']=True
		session['name']=form.name.data
		form.name.data=''
		odd_name=session.get('name')
		'''if odd_name is not None and odd_name != form.name.data :
			flash("You have changed your name!")
		session['name']=form.name.data'''
		return redirect(url_for('.login'))
	return render_template('/login.html',form=form,name=session.get('name'),known = session.get('known',False))
