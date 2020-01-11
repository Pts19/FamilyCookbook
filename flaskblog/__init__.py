import os
#Just to use os.path.join and os.path.dirname
from flask import Flask
#Used to import Flask application files for app creation
from flask_sqlalchemy import SQLAlchemy
#Import flask version of SQLAlchemy -> import specifically flask-SQLAlchemy

from flask_bcrypt import Bcrypt
from flask_login import LoginManager
#Flask modules for Encryption - Bcrypt
#Flask modules for Login Manager - Valid email - matching passwords ect.

from flask_mail import Mail
import smtplib


project_dir = os.path.dirname(os.path.abspath(__file__))
#Find path to specific project directory for cat with database location
database_file = "sqlite:///{}".format(os.path.join(project_dir, "site.db"))
#Compound project directory path with sqlite:/// to tell
#SQLAlchemy which databse engine we are using - Flask - SQLAlchemy

app = Flask(__name__)
#Main app inialization with special __name__ var to let
#flask intelligently configure app

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
#Tell our web application specifically where our databse will be stored

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
#Secret web_token? Need further reading and implementation

db = SQLAlchemy(app)
#Initilaize connection to database
#Keep this in the DB variable, Use -DB- to interact with database

bcrypt = Bcrypt(app)
#Bcrypt initialization to app object.
#Will use Bcrypt for storage of keys, passwords, ---

login_manager = LoginManager(app)

login_manager.login_view = 'login'
#pass in function name of route, just like url_for('home')
#Login Page - '/login'
#May pass different login page template for admins vs. regular users?

login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True

app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')


mail = Mail(app)

from flaskblog import routes
#Must be an import at end of file as routes.py imports rely
#on app, db, login_manager initialization to run application
