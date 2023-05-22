from flask import render_template, request
from app.posts import bp
from app.extensions import db
from app.models.post import Post

# Items per page
items_per_page = 2


@bp.route('/')
def index():

    # Get page number from the URL query string
    page = int(request.args.get('page', 1))

    # Calculate the offset for pagination
    offset = (page - 1) * items_per_page

    # Fetch items from the database
    posts = Post.query.order_by(Post.id.desc()).limit(items_per_page).offset(offset).all()

    total_items = Post.query.count()

    # Calculate the total number of pages
    total_pages = (total_items + items_per_page - 1) // items_per_page

    return render_template('posts/index.html', posts=posts, page=page, total_pages=total_pages)


@bp.route('/categories/')
def categories():
    return render_template('posts/categories.html')


@bp.route('/content/<int:post_id>')
def content(post_id):
    # Fetch the item from the database
    post = Post.query.get(post_id)

    return render_template('posts/content.html', post=post)
