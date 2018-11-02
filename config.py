import os
import environ_var

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRECT_KKEY=os.environ.get('SECRET_KEY') or 'hard to guess string'
    MAIL_SERVER = os.environ.get('MAIL_SERVER','smtp.qq.com')
    MAIL_PORT = int (os.environ.get('MAIL_PORT','587'))
    MAIL_USE_TLS=os.environ.get('MAIL_USE_TLS','true').lower() in ['true','on','1']


    MAIL_USERNAME=environ_var.MAIL_USERNAME #should be in environ
    MAIL_PASSWORD=environ_var.MAIL_PASSWORD
    FLASKY_MAIL_SUBJECT_PREFIX ='[Flasky]'
    FLASKY_MAIL_SENDER='Flasky Admin <1091491336@qq.com>'
    FLASKY_ADMIN=os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

	#email
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):#succeed class Config
    DEBUG=True
    SQLALCHEMY_DATABASE_URI=os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
class TestingConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
config={
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,
    'default':DevelopmentConfig
}
