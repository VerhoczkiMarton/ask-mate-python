from flask import Flask, render_template, request, redirect, url_for
import data_manager
import connection

app = Flask(__name__)
questions = data_manager.get_questions()
answers = data_manager.get_answers()
QUESTION_HEADERS = connection.get_headers('questions')
ANSWER_HEADERS = connection.get_headers('answers')


@app.route('/list')
def route_list():
    questions = data_manager.get_questions()
    return render_template('list.html', questions=questions)

    pass


@app.route('/question/<question_id>')
def display_question(question_id):
    question = questions[question_id]
    return render_template('question.html', question=question, question_id=question_id, question_headers=QUESTION_HEADERS)


@app.route('/add-question')
def add_question():
    pass


if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=8000
    )