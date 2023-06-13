import os
from app.extensions import db
from app.models.post import ScrapedPost as Blog

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.methods import media, posts


def scheduled_push_blog():

    with db.app.app_context():
        blogs = Blog.query.filter_by(processed=False).all()
        for blog in blogs:
            publish_to_wordpress(blog)
            blog.processed = True

        db.session.commit()


def publish_to_wordpress(blog):
    # 从 .env 文件中读取 WordPress 配置信息
    wordpress_url = os.getenv('WORDPRESS_URL')
    wordpress_username = os.getenv('WORDPRESS_USERNAME')
    wordpress_password = os.getenv('WORDPRESS_PASSWORD')

    # 创建 WordPress 客户端
    print(wordpress_url, wordpress_username, wordpress_password)
    client = Client(wordpress_url, wordpress_username, wordpress_password)

    blog_title, blog_article = get_blog_content(blog)
    # 创建 WordPress 文章对象
    post = WordPressPost()
    post.title = blog_title
    post.content = blog_article
    post.post_status = 'draft'  # 文章状态，不写默认是草稿，private表示私密的，draft表示草稿，publish表示发布
    post.terms_names = {
        'post_tag': [],  # 文章所属标签，没有则自动创建
        'category': [blog.category]  # 文章所属分类，没有则自动创建
    }

    # default news featured image ID
    post.thumbnail = 1270

    # 发布文章
    client.call(NewPost(post))
    return


def get_blog_content(blog):

    blog_title = blog.title

    blog_article = blog.img_href + '\n' + blog.article + '\n' + blog.href

    return blog_title, blog_article
