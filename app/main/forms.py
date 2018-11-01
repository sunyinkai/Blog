from flask_wtf import Form
from wtforms import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, AnyOf

class NameForm(Form): #define a form
	name=StringField('username',validators=[DataRequired(u'please input the valid user id!')])
	password=PasswordField('password',validators=[DataRequired(message=u'Please input the correct password!')])
	remeber_me=BooleanField('remerber me',default=False)
	submit= SubmitField(u'Login')
