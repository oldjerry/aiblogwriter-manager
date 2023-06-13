from flask import render_template, request, url_for, redirect
from app.blog import bp
from app.extensions import db
from app.models.blog import ScrapedBlog as Blog

from app.autotasks.push_blog import scheduled_push_blog

# Items per page
items_per_page = 10


@bp.route('/')
def index():

    # Get page number from the URL query string
    page = int(request.args.get('page', 1))

    # Calculate the offset for pagination
    offset = (page - 1) * items_per_page

    # Fetch items from the database
    blogs = Blog.query.order_by(Blog.gen_time.desc()).limit(items_per_page).offset(offset).all()

    total_items = Blog.query.count()

    # Calculate the total number of pages
    total_pages = (total_items + items_per_page - 1) // items_per_page

    return render_template('blog/index.html', blogs=blogs, page=page, total_pages=total_pages)


@bp.route('/content/<int:blog_id>')
def content(blog_id):
    # Fetch the item from the database
    blog = Blog.query.get(blog_id)

    return render_template('blog/content.html', blog=blog)


@bp.route('/push/', methods=['GET', 'POST'])
def push_post():
    # Fetch the item from the database
    if request.method == 'POST':
        scheduled_push_blog()

    return redirect(url_for('blog.index'))
