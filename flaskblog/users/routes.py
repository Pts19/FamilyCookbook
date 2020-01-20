from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email


users = Blueprint('users', __name__)

"""
    localhost:5000/register
    Accepts GET and POST methods
"""
@users.route('/register', methods=['GET', 'POST'])
def register():
    #Once user is_authenticated -> redirect to home using url_for
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    """
        Use RegistrationForm() -> Accepts:
            form.password.data
                bcrypt.generate_password with 128bit hash encryption
                decode with utf-8 to remove b' xxxxxxxxxxxx ' from password
    """
    if form.validate_on_submit(): #Flash a message after created account
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to login!', 'success')#LOOK UP
        return redirect(url_for('users.login'))#function name for def home(): ^^
    return render_template('register.html', title='Register', form=form)

"""
    localhost:5000/login
    Accepts GET and POST methods
"""
@users.route('/login', methods=['GET','POST'])
def login():
    #Once user is_authenticated -> redirect to home using url_for
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    """
        Accepts email(stringField), password(passField), amd remember(bool)
        Remember Me: WORK ON THIS -> Populate form.email.data with current_user Email
        Must validate and prove current user with browser token?
    """
    if form.validate_on_submit():
        #Query filter_by first email match -> then set user var to entire User data struct
        user = User.query.filter_by(email=form.email.data).first()
        #if user is populated, that means user email exists.
        #Then use bcrypt.check_password_hash to check if form.data matches user.password
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            #Log them in when validated
            login_user(user, remember=form.remember.data)
            """
                if redirected here from @login_required pages
                ->  Track ?next=xxxxxxx and store it in next_page var
                    Take next_page and use it in ternary single line
            """
            next_page = request.args.get('next')
            """
                Use args.get() instead of args[] like an array
                args[] will throw error if no next key
                args.get() will return 'none' if no next key
            """
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
            #ternary (do -> if true, else -> so something else)
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            #Flash message for unsuccessful -> Do not reveal is user/pass is wrong.
    return render_template('login.html', title='Login', form=form)



"""
    localhost:5000/logout
    simple logout method
    sent here on logout button press
"""
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))



"""
    localhost:5000/account
    The account function provides the support to change account info.
    The account info that can be changed is: username, email, and profile pic
    TODO -> Add ability to reset password
            Change password
            Change email linked to account.
"""
@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    """
        Show ^UpdateAccountForm()^
        Once form is validated:
            resize and save picture if form.picture.data is populated
            current_user name and email = form.name/email.data
                This is simply way to update data in database
            flash confirmation message stating successful info update
    """
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    """
        On GET request:
            autofill in form.username.data with current_user.username
            autofill in form.email.data with current_user.email
        Display the current profile pic by fetching picture from:
            static/profile_pics/+ current_user.Image_file
                -> This will always display most updated image
    """
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)



"""
    localhost:5000/user/string
        where 'string' is the username of the specific user

        set default page to page 1 and the pages are of type int
        find first user using username passed to user_posts() function

        query for all posts by user
            ordered by date_descending and
            paginate 5 posts per page
"""
@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)



@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))

    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    #This will receive the user_id if it matches the token
    user = User.verify_reset_token(token)
    if user is None:
        flash('This is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit(): #Flash a message after created account
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to login', 'success')#LOOK UP
        return redirect(url_for('users.login'))#function name for def home(): ^^
    return render_template('reset_token.html', title='Reset Password', form=form)
