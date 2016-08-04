# -*- coding: utf-8 -*-
from flask import redirect,url_for,request,flash
from flask import render_template
from .forms import LoginForm,RegisterForm
from flask.ext.login import login_user,login_required,logout_user,current_user
from ..models import User
from ..main import main
from .. import db

from . import auth

@auth.before_app_request
def before_request():
	if current_user.is_authenticated\
	   and not current_user.confirmed \
	   and request.endpoint[:5]!='auth.'\
	   and request.endpoint!='static':
	  	return redirect(url_for('auth.unconfirmed'))

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
	  	user = User.query.filter_by(email=form.email.data).first()
	   	if user is not None and user.vertify_password(form.password.data):
	   		login_user(user,form.remember_me.data)
	   		return redirect(request.args.get('next') or url_for('main.index'))
	   	flash(u'无效的用户名或密码')
    return render_template('auth/login.html',form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('main.index'))

@auth.route('/register',methods=['GET','POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		user = User(email=form.email.data,
					username=form.username.data,
					password=form.password.data)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('main.index'))
	return render_template('auth/register.html',form=form)
