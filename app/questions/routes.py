from flask import render_template, request, url_for, redirect
from app.questions import bp
from app.extensions import db
from app.models.question import Question


@bp.route('/', methods=('GET', 'POST'))
def index():
    questions = Question.query.all()

    if request.method == 'POST':
        new_question = Question(content=request.form['content'],
                                answer=request.form['answer'])
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for('questions.index'))

    return render_template('questions/index.html', questions=questions)
