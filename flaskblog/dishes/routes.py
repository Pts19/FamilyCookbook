from flask import render_template, request, Blueprint
from flaskblog.models import Post

dishes = Blueprint('dishes', __name__)



@dishes.route('/chicken')
def chicken():
    protein="Chicken"
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(mainIngredient=protein)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('dishes.html', posts=posts, protein=protein)

"""
    localhost:5000/about
    Contentless /about page for html templating for layouts.html extension
    and for easy copy pastring if future route additions
"""
@dishes.route('/top5')
def top5():
    topDishes=[30, 29, 18, 26, 17]
    #page = request.args.get('page', 1, type=int)
    post1 = Post.query.get_or_404(topDishes[0])
    post2 = Post.query.get_or_404(topDishes[1])
    post3 = Post.query.get_or_404(topDishes[2])
    post4 = Post.query.get_or_404(topDishes[3])
    post5 = Post.query.get_or_404(topDishes[4])

    return render_template('top5.html', post1=post1, post2=post2, post3=post3, post4=post4, post5=post5)

@dishes.route('/beef')
def beef():
    protein="Beef"
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(mainIngredient=protein)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('dishes.html', posts=posts, protein=protein)

@dishes.route('/dinner')
def dinner():
    mealType="Dinner"
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(mealType=mealType)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('mealType.html', posts=posts, mealType=mealType)

@dishes.route('/breakfast')
def breakfast():
    mealType="Breakfast"
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(mealType=mealType)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('mealType.html', posts=posts, mealType=mealType)



#enddishes
