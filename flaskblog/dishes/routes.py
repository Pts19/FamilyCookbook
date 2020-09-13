from flask import render_template, request, Blueprint
from flaskblog.models import Post

dishes = Blueprint('dishes', __name__)

@dishes.route('/chicken')
def chicken():
    protein="chicken"
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('dishes.html', posts=posts, protein=protein)

"""
    localhost:5000/about
    Contentless /about page for html templating for layouts.html extension
    and for easy copy pastring if future route additions
"""
@dishes.route('/top5')
def top5():
    protein="Top 5"
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('dishes.html', posts=posts, protein=protein)

@dishes.route('/beef')
def beef():
    protein="beef"
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('dishes.html', posts=posts, protein=protein)

@dishes.route('/dinner')
def dinner():
    return render_template('about.html', title='About')



#enddishes
