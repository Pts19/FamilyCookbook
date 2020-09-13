from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

posts = Blueprint('posts', __name__)

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
@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm() #Object creation to act on the PostForm class
    if form.validate_on_submit():
        post = Post(title=form.title.data, mealType=form.mealType.data,
                    mainIngredient=form.mainIngredient.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                            form=form, legend='New Post')

"""
    localhost:5000/post/#
        where '#' is equal to the specific post_id
    grab a post by using -> query.get_or_404(post_id)
        where post_id is passed to post() function

    render this post using the post.html template, title=post.title
"""
@posts.route('/post/<int:post_id>')
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
@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403) #Forbidden route HTTP response -> Will customize later
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.mealType = form.mealType.data
        post.mainIngredient = form.mainIngredient.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.mealType.data = post.mealType
        form.mainIngredient.data = post.mainIngredient
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
@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
