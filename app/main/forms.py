from flask_wtf import Form
from wtforms import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import Required, Email, AnyOf
class NameForm(Form): #define a form
	name=StringField('username',validators=[Required(u'please input the valid user id!')])
	password=PasswordField('password',validators=[Required(message=u'Please input the correct password!')])
	remeber_me=BooleanField('remerber me',default=False)
	submit= SubmitField(u'Login')
