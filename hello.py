from flask import Flask,render_template,redirect,session,url_for,flash
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField,BooleanField,SubmitField
from wtforms.validators import Required,Email,AnyOf


app = Flask(__name__)
bootstrap=Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'
class NameForm(Form): #define a form
	name=StringField('what is your name?',validators=[Required()])
	submit= SubmitField('Submit')

@app.route('/',methods=['GET','POST'])
def index():
	name=None
	form=NameForm()
	if form.validate_on_submit():
		odd_name=session.get('name')
		if odd_name is not None and odd_name != form.name.data :
			flash("You have changed your name!")
		session['name']=form.name.data
		return redirect(url_for('index'))
	return render_template('index.html',form=form,name=session.get('name'))

@app.route('/user/<name>')
def user(name):
	return render_template('user.html',name=name)

#deal the error
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html')
@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html')
if  __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
