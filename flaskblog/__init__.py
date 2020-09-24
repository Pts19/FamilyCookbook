from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config

#app = Flask(__name__)
#Main app inialization with special __name__ var to let
#flask intelligently configure app

db = SQLAlchemy()
#Initilaize connection to database
#Keep this in the DB variable, Use -DB- to interact with database

bcrypt = Bcrypt()
#Bcrypt initialization to app object.
#Will use Bcrypt for storage of keys, passwords, ---

login_manager = LoginManager()
login_manager.login_view = 'users.login'
#pass in function name of route, just like url_for('home')
#Login Page - '/login'
#May pass different login page template for admins vs. regular users?

login_manager.login_message_category = 'info'
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.dishes.routes import dishes
    from flaskblog.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(dishes)
    app.register_blueprint(errors)

    return app
