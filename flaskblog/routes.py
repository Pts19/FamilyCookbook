import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt, mail
from flaskblog.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                             PostForm, RequestResetForm, ResetPasswordForm)
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


"""
    localhost:5000/    or    localhost:5000/home
    No get/post methods required

    default page = 1
    page = pageNumber from args.get()
        -> http://127.0.0.1:5000/home?page=2
           get all args after 'page' -> button clicks below posts
    posts = all posts on page = X, posts per_page = 3
        -> Sort all these posts by date_descending (newest posts first!)
"""
@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('home.html', posts=posts)

"""
    localhost:5000/about
    Contentless /about page for html templating for layouts.html extension
    and for easy copy pastring if future route additions
"""
@app.route('/about')
def about():
    return render_template('about.html', title='About')


"""
    localhost:5000/register
    Accepts GET and POST methods
"""
@app.route('/register', methods=['GET', 'POST'])
def register():
    #Once user is_authenticated -> redirect to home using url_for
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
        return redirect(url_for('login'))#function name for def home(): ^^
    return render_template('register.html', title='Register', form=form)

"""
    localhost:5000/login
    Accepts GET and POST methods
"""
@app.route('/login', methods=['GET','POST'])
def login():
    #Once user is_authenticated -> redirect to home using url_for
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
            return redirect(next_page) if next_page else redirect(url_for('home'))
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
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

"""
    save_picture() takes in jpg or png for resize and saving:
        get random_hex for naming of the new-resized picture
        get the extension of the picture passed to function -> png/jpg
        combine random hex with file_ext for renaming and saving
        create picture_path that possess correct file path for picture
            -> Path to current flaskblog project, then static/profile_pics
        Read comments below for resizing schem
"""
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    #use '_' for total throwaway variable -> only want file_extension
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    """
        output_size is a tuple holding (dimensions of the new thumbnail)
        i object is set to the form.picture from the form UpdateAccountForm()
        use PIL(pillow) to craft thumbnail of the image using the size tuple
        save resized image using picture_path
    """
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    #return picture to Update account function save orignal picture
    return picture_fn

"""
    localhost:5000/account
    The account function provides the support to change account info.
    The account info that can be changed is: username, email, and profile pic
    TODO -> Add ability to reset password
            Change password
            Change email linked to account.
"""
@app.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('account'))
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
    localhost:5000/post/new
    The form used on new posts in PostForm()
    If entire form is valid on submit:
        Fetch TITLE and CONTENT from form.data
        Post.author = current_user
            -> This is used for One-to-Many relationship between
               User and Posts -> One author can have many posts
        Save new post to database -> Then commit those changes
"""
@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm() #Object creation to act on the PostForm class
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                            form=form, legend='New Post')

"""
    localhost:5000/post/#
        where '#' is equal to the specific post_id
    grab a post by using -> query.get_or_404(post_id)
        where post_id is passed to post() function

    render this post using the post.html template, title=post.title
"""
@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

"""
    localhost:5000/post/#/update
        where '#' is equal to the specific post_id

        grab a post by using -> query.get_or_404(post_id)
        where post_id is passed to update_post() function

        Verifiy that current_user = post.author
            abort(403) -> Forbidden route -> HTTP response
        Use the PostForm() form from forms.py

        grab updated title and content from form.title/content.data
            Then commit these changes
        Flash a success message, then redirect the user to the updated post

    render this post using the creat_post.html template, title=Update Post
"""
@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403) #Forbidden route HTTP response -> Will customize later
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    """
        On GET request:
            autofill in form.title.data with post.title
            autofill in form.content.data with post.content
    """
    return render_template('create_post.html', title='Update Post',
                            form=form, legend='Update Post')


"""
    localhost:5000/post/#/delete
        where '#' is equal to the specific post_id

        grab a post by using -> query.get_or_404(post_id)
        where post_id is passed to delete_post() function

        Verifiy that current_user = post.author
            abort(403) -> Forbidden route -> HTTP response

        db.session.delete(post) -> db.session.commit()
        flash confirmation message for successful deletion
        redirect user to home page
"""
@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


"""
    localhost:5000/user/string
        where 'string' is the username of the specific user

        set default page to page 1 and the pages are of type int
        find first user using username passed to user_posts() function

        query for all posts by user
            ordered by date_descending and
            paginate 5 posts per page
"""
@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                   sender='patricksheehancs@gmail.com',
                   recipients=[user.email])
    #_external=True discussed at 33:15 Episode:10
    msg.body = f'''To reset you password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made
'''
    mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))

    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    #This will receive the user_id if it matches the token
    user = User.verify_reset_token(token)
    if user is None:
        flash('This is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit(): #Flash a message after created account
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to login', 'success')#LOOK UP
        return redirect(url_for('login'))#function name for def home(): ^^
    return render_template('reset_token.html', title='Reset Password', form=form)

#end
