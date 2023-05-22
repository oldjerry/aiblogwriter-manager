from flask import render_template, request
from app.news import bp
from app.extensions import db
from app.models.news import ScrapedNews as News

# Items per page
items_per_page = 10


@bp.route('/')
def index():

    # Get page number from the URL query string
    page = int(request.args.get('page', 1))

    # Calculate the offset for pagination
    offset = (page - 1) * items_per_page

    # Fetch items from the database
    newses = News.query.order_by(News.gen_time.desc()).limit(items_per_page).offset(offset).all()

    total_items = News.query.count()

    # Calculate the total number of pages
    total_pages = (total_items + items_per_page - 1) // items_per_page

    return render_template('news/index.html', newses=newses, page=page, total_pages=total_pages)


@bp.route('/content/<int:news_id>')
def content(news_id):
    # Fetch the item from the database
    news = News.query.get(news_id)

    return render_template('news/content.html', news=news)
