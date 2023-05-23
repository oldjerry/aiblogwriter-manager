import os
from dotenv import load_dotenv, find_dotenv
from app.autotasks.push_news import scheduled_push_news


basedir = os.path.abspath(os.path.dirname(__file__))


# load environmental variable from .env with python-dotenv
load_dotenv(find_dotenv(), verbose=True)


class Config:
    # set SECRET_KEY
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # load SQLite data file
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JOBS = [
        {
            "id": "push-news-job",
            "func": scheduled_push_news,
            "trigger": "interval",
            "seconds": 30
        }
    ]