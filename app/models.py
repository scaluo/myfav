# -*- coding: utf-8 -*-
from . import db
from . import login_manager
from datetime import datetime
from itsdangerous import JSONWebSignatureSerializer as Serializer
from flask import current_app
from flask.ext.login import UserMixin
from werkzeug.security import  generate_password_hash,check_password_hash
from goose import Goose
from goose.text import StopWordsChinese

class Fav(db.Model):
	__tablename__ = 'favs'
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(255))
	url = db.Column(db.String(255))
	summary = db.Column(db.String(200))
	body = db.Column(db.Text)
	timestamp = db.Column(db.DateTime,index=True,default=datetime.now)
	author_id = db.Column(db.Integer,db.ForeignKey('users.id'))

	def __init__(self,url,author):
 		self.url = url
		self.author = author
		goose = Goose({'stopwords_class': StopWordsChinese})
		article = goose.extract(url=url)
		if article.title == '':
			goose = Goose()
			article = goose.extract(url=url)
		self.title = article.title
		self.summary = article.cleaned_text[:150]
		self.body = article.cleaned_text

class User(UserMixin,db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer,primary_key=True)
	email = db.Column(db.String(64),unique=True,index=True)
	username = db.Column(db.String(64),unique=True,index=True)
	password_hash = db.Column(db.String(128))
	#默认为已经确认
	confirmed = db.Column(db.Boolean,default=True)
	favs = db.relationship('Fav',backref='author',lazy='dynamic')

	@property
	def password(self):
	    raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self,password):
		self.password_hash = generate_password_hash(password)

	def vertify_password(self,password):
		return check_password_hash(self.password_hash,password)

	def generate_confirmation_token(self,expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'])
		return s.dumps({'confirm':self.id})

	def confirm(self,token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return false

		if data.get('confirm') != self.id:
			return false
		self.confirmed = True
		db.session.add(self)
		return True

	def __repr__(self):
		return '<User %r>'%self.username

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
