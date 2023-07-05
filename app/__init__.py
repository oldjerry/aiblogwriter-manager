import os
from flask import Flask
from config import Config
from app.extensions import db
from app.main import bp as main_bp

from app.news import bp as news_bp
from app.blog import bp as blog_bp
# from app.questions import bp as questions_bp

from app.autotasks.push_news import scheduled_push_news
from app.autotasks.push_blog import scheduled_push_blog


from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


def create_app(config_class=Config):
    app = Flask(__name__)

    # load Config
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.app = app
    db.init_app(app)

    # Register blueprints here
    app.register_blueprint(main_bp)
    app.register_blueprint(news_bp, url_prefix='/news')
    app.register_blueprint(blog_bp, url_prefix='/blog')
    # app.register_blueprint(questions_bp, url_prefix='/questions')

    # Register apscheduler tasks
    scheduler = BackgroundScheduler()

    scheduler.add_job(scheduled_push_blog, trigger=CronTrigger(hour=11, minute=50))
    scheduler.add_job(scheduled_push_news, trigger=CronTrigger(hour=11, minute=55))

    scheduler.start()

    return app
