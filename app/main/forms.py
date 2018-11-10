from flask_wtf import Form
from wtforms import StringField, BooleanField, SubmitField, PasswordField,TextAreaField
from wtforms.validators import DataRequired, Email, AnyOf,Length

class NameForm(Form): #define a form
	name=StringField('username',validators=[DataRequired(u'please input the valid user id!')])
	password=PasswordField('password',validators=[DataRequired(message=u'Please input the correct password!')])
	remeber_me=BooleanField('remerber me',default=False)
	submit= SubmitField(u'Login')

class EditProfileForm(Form):
	name=StringField('Real name',validators=[Length(0,64)])
	location=StringField('Location',validators=[Length(0,64)])
	about_me=TextAreaField('About me')
	sumbit=SubmitField('submit')
