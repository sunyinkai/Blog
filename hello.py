from flask import Flask,render_template
from flask import redirect
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField,BooleanField
from wtforms.validators import Required


app = Flask(__name__)
bootstrap=Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'
class NameForm(Form): #define a form
	name=StringField('what is your name?',validators=[Required()])
	submit= BooleanField('Submit')

@app.route('/',methods=['GET','POST'])
def index():
	name=None
	form=NameForm()
	if form.validate_on_submit():
		name=form.name.data
		form.name.data=''
	return render_template('index.html',form=form,name=name)

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
