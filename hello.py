from flask import Flask,render_template,redirect,session,url_for,flash
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField,BooleanField,SubmitField,PasswordField
from wtforms.validators import Required,Email,AnyOf
from flask_sqlalchemy import SQLAlchemy
import os
from flask_script import Manager,Shell
basedir =os.path.abspath(os.path.dirname(__file__)) #the database

app = Flask(__name__)
manager = Manager(app)
app.config['SQLALCHEMY_DATABASE_URI']=\
'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
db=SQLAlchemy(app) # create an SQLAlchemy Object

class Role(db.Model):
	__tablename__ ='roles'
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(64),unique=True)
	users = db.relationship('User',backref='role')
	def __repr__(self):
		return '<Role %r>' %self.name


class User(db.Model):
	__tablename__='users'
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(64),unique=True,index=True)
	role_id= db.Column(db.Integer,db.ForeignKey('roles.id'))
	def __repr__(self):
		return '<User %r>' % self.username

bootstrap=Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'
class NameForm(Form): #define a form
	name=StringField('username',validators=[Required(u'please input the valid user id!')])
	password=PasswordField('password',validators=[Required(message=u'Please input the correct password!')])
	remeber_me=BooleanField('remerber me',default=False)
	submit= SubmitField(u'Login')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
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
		return redirect(url_for('login'))
	return render_template('/login.html',form=form,name=session.get('name'),known = session.get('known',False))

#deal the error
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html')
@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html')

def make_shell_context():
	return dict(app=app,db=db,User=User,Role=Role)
if  __name__ == '__main__':
	#manager.add_command("shell",Shell(make_context=make_shell_context))
	#manager.run()
    app.run(host='0.0.0.0',port=5000)
