import os
from dotenv import load_dotenv, find_dotenv


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
