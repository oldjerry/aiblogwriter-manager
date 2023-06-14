import os
from app.extensions import db
from app.models.news import ScrapedNews as News

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import media, posts
from wordpress_xmlrpc.methods.posts import NewPost


def scheduled_push_news():

    with db.app.app_context():
        news_list = News.query.filter_by(processed=False).all()
        for news in news_list:
            publish_to_wordpress(news)
            news.processed = True

        db.session.commit()


def publish_to_wordpress(news):
    # 从 .env 文件中读取 WordPress 配置信息
    wordpress_url = os.getenv('WORDPRESS_URL')
    wordpress_username = os.getenv('WORDPRESS_USERNAME')
    wordpress_password = os.getenv('WORDPRESS_PASSWORD')

    # 创建 WordPress 客户端
    print(wordpress_url, wordpress_username, wordpress_password)
    client = Client(wordpress_url, wordpress_username, wordpress_password)

    news_title, news_article = get_news_content(news)
    # 创建 WordPress 文章对象
    post = WordPressPost()
    post.title = news_title
    post.content = news_article
    post.post_status = 'draft'  # 文章状态，不写默认是草稿，private表示私密的，draft表示草稿，publish表示发布
    post.terms_names = {
        'post_tag': [],  # 文章所属标签，没有则自动创建
        'category': ['News', news.category]  # 文章所属分类，没有则自动创建
    }

    # default news featured image ID
    post.thumbnail = 1270

    # 发布文章
    client.call(NewPost(post))
    return


def get_news_content(news):

    news_title = news.title

    news_article = news.img_href + '\n' + news.article + '\n' + news.href

    return news_title, news_article
