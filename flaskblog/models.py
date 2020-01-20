from flask import current_app
from flaskblog import db, login_manager
#import pytz USE IF datetime.utcnow does not work for timezone - CST
#pip install pytz
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Simple User Model -> May add creation date, rolling post total, Karma??
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    #ONE TO MANY RELATIONSHIP INC \/
    posts = db.relationship('Post', backref='author', lazy=True)
    #Lazy-True???
    #backref = basically new column for all posts by a user
    #'Post' -> actually reference class Post, not the table for posts

    #30min expiration on token
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self): #MAGIC METHOD FOR FORMATING LOOK UP RESEARCH
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    #date_posted = db.Column(db.DateTime, nullable=False,
                            #default=datetime.now(pytz.timezone('Chicago')))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #ForeignKey reference actually table for user, not User class

    def __repr__(self): #MAGIC METHOD FOR FORMATING LOOK UP RESEARCH
        return f"Post('{self.title}', '{self.date_posted}')"
