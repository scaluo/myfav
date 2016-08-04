# -*- coding: utf-8 -*- 
from flask.ext.wtf import Form
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import Required

class UrlForm(Form):
	url = StringField(u'链接地址',validators=[Required()])
	submit = SubmitField(u'保存')
