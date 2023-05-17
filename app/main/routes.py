from flask import render_template
from app.main import bp


@bp.route('/')
def index():
    return render_template('index.html')


# @bp.route('/test/')
# def test():
#     return '<h1>Testing the Flask Application Factory Pattern</h1>'
