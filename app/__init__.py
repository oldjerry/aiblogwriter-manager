from flask import Flask
from config import Config
from app.extensions import db
from app.main import bp as main_bp
from app.posts import bp as posts_bp
from app.questions import bp as questions_bp


def create_app(config_class=Config):
    app = Flask(__name__)

    # load Config
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)

    # Register blueprints here
    app.register_blueprint(main_bp)
    app.register_blueprint(posts_bp, url_prefix='/post')
    app.register_blueprint(questions_bp, url_prefix='/questions')

    # @app.route('/test/')
    # def test_page():
    #     return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app
