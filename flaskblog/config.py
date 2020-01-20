import os
from flask_sqlalchemy import SQLAlchemy
#Import flask version of SQLAlchemy -> import specifically flask-SQLAlchemy

class Config:
    project_dir = os.path.dirname(os.path.abspath(__file__))
    #Find path to specific project directory for cat with database location
    database_file = "sqlite:///{}".format(os.path.join(project_dir, "site.db"))
    #Compound project directory path with sqlite:/// to tell
    #SQLAlchemy which databse engine we are using - Flask - SQLAlchemy

    SQLALCHEMY_DATABASE_URI = database_file
    #Tell our web application specifically where our databse will be stored

    #SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = "5791628bb0b13ce0c676dfde280ba245"
    #Secret web_token? Need further reading and implementation
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True

    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
