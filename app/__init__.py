import os
from flask import Flask
from config import Config
from app.extensions import db
from app.main import bp as main_bp

from app.news import bp as news_bp
from app.blog import bp as blog_bp
from app.questions import bp as questions_bp


from flask_apscheduler import APScheduler
from apscheduler.triggers.interval import IntervalTrigger


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
    scheduler = APScheduler()

    scheduler.init_app(app)

    # # 解决FLASK DEBUG模式定时任务执行两次
    # if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    #     scheduler.api_enabled = True
    #     scheduler.init_app(app)
    #     # 实例话interval对象，如果不实例话的话有可能会报错没有interval这个
    #     # interval = IntervalTrigger(
    #     #     days=2,
    #     #     start_date='2019-4-24 08:00:00',
    #     #     end_date='2099-4-24 08:00:00',
    #     #     timezone='Asia/Shanghai')
    #     interval = IntervalTrigger(
    #         seconds=3,
    #     )
    #     scheduler.add_job(func=scheduled_push_news, trigger=interval, id='test_one')

    # scheduler.start()

    return app
