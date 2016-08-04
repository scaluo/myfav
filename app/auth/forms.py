# -*- coding: utf-8 -*- 
from flask.ext.wtf import Form
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required,Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(Form):
	email = StringField('Email',validators=[Required(),Length(1,64),Email()])
	password = PasswordField('Password',validators=[Required()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Login in')

class RegisterForm(Form):
	email = StringField('Email',validators=[Required(),Length(1,64),Email()])
	username = StringField('Username',validators=[Required(),Length(1,64),Regexp('^[A-Za-z0-9_.]*$',0,'Username must only letters,numbers,dots or underscore')])
	password = PasswordField('Password',validators=[
			   Required(),EqualTo('password2',message='password is not equal')])
	password2 = PasswordField('Confirm password',validators=[Required()])

	submit = SubmitField('Register')

	def validate_email(self,field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email is already exists')

	def validate_username(self,field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('Username is already exists')
