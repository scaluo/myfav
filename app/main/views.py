# -*- coding: utf-8 -*-
from flask import render_template,redirect,url_for,request
from flask.ext.login import current_user,login_required
from . import main
from .forms import UrlForm
from ..models import Fav
from .. import db


@main.route('/',methods=['GET','POST'])
def index():
	if not current_user.is_authenticated:
		return redirect(url_for('auth.login'))
		
	form = UrlForm()
	if form.validate_on_submit():
		url = form.url.data
		fav = Fav(url=url,
					author=current_user._get_current_object())
		db.session.add(fav)
		return redirect(url_for('.index'))
	page = request.args.get('page',1,type=int)
	pagination = Fav.query.order_by(Fav.timestamp.desc()).paginate(page,per_page=10,error_out=False)
	favs = pagination.items
	return render_template('index.html',form=form,favs=favs,pagination=pagination)

@main.route('/delfav/<int:id>')
@login_required
def del_fav(id):
	fav = Fav.query.get_or_404(id)
	db.session.delete(fav)
	return redirect(url_for('.index'))
