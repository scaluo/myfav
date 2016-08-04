# -*- coding: utf-8 -*- 
from flask.ext.wtf import Form
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required,Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(Form):
	email = StringField(u'邮箱',validators=[Required(),Length(1,64),Email()])
	password = PasswordField(u'密码',validators=[Required()])
	remember_me = BooleanField(u'记住我')
	submit = SubmitField(u'登录')


class RegisterForm(Form):
	email = StringField(u'邮箱',validators=[Required(),Length(1,64),Email()])
	username = StringField(u'昵称',validators=[Required(),Length(1,64),Regexp('^[A-Za-z0-9_.]*$',0,u'昵称必须是字母，数字，点或下划线')])
	password = PasswordField(u'密码',validators=[
			   Required(),EqualTo('password2',message=u'密码不一致')])
	password2 = PasswordField(u'密码确认',validators=[Required()])

	submit = SubmitField(u'注册')

	def validate_email(self,field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError(u'邮箱已使用')

	def validate_username(self,field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError(u'昵称已存在')
