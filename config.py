# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__name__))

class Config:
	SECRET_KEY = "i can run fast"
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True

	@staticmethod
	def init_app(app):
		pass


class DevelopmentConfig(Config):
	DEBUG = True
	MAIL_DEBUG = True
	SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir,'data-dev.sqlite')
	BOOTSTRAP_SERVE_LOCAL = True

config = {
	'development': DevelopmentConfig
}
