from flask import Flask, render_template, request, redirect, url_for
import data_manager
import connection
import util
import uuid
import datetime


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
    answers_for_question = util.get_answers_for_question_id(question_id, answers)
    return render_template('question.html', question=question, question_id=question_id, answers=answers_for_question)

@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def new_answer(question_id):
    if request.method == 'POST':
        new_answer = dict()
        id = str(uuid.uuid4())
        new_answer['submission_time'] = datetime.datetime.now().timestamp()
        new_answer['vote_number'] = 0
        new_answer['question_id'] = question_id
        new_answer['message'] = request.form.get('message')
        new_answer['image'] = None
        global answers
        answers.update({id : new_answer})
        connection.write_all_answers(answers)
        answers = data_manager.get_answers()
        return redirect(f'/question/{question_id}')
    else:
        return render_template('new_answer.html',question_id=question_id )


@app.route('/add-question')
def add_question():
    pass


if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=8000
    )