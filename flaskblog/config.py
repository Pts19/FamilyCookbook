import os
from flask_sqlalchemy import SQLAlchemy
#Import flask version of SQLAlchemy -> import specifically flask-SQLAlchemy

class Config:    
    #SQLAlchemy which databse engine we are using - Flask - SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    #Tell our web application specifically where our databse will be stored

    SECRET_KEY = os.environ.get('SECRET_KEY')

    #Secret web_token? Need further reading and implementation
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True

    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
