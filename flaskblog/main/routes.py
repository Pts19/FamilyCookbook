from flask import render_template, request, Blueprint
from flaskblog.models import Post

main = Blueprint('main', __name__)

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
@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('home.html', posts=posts)

"""
    localhost:5000/about
    Contentless /about page for html templating for layouts.html extension
    and for easy copy pastring if future route additions
"""
@main.route('/about')
def about():
    return render_template('about.html', title='About')


#endmain
