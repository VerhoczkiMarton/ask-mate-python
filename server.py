from flask import Flask, render_template, request, redirect, url_for
import data_manager
import connection
import util
import uuid
from datetime import datetime

app = Flask(__name__)


questions = data_manager.get_questions()
answers = data_manager.get_answers()

QUESTION_HEADERS = ['Submission time', 'View number', 'Vote number', 'Title', 'Message', 'Image']
ANSWER_HEADERS = ['Submission time', 'Vote number', 'Question id', 'Message', 'Image']

@app.route('/')
@app.route('/list')
def route_list():
    global questions
    questions = data_manager.get_questions()
    order_by = request.args.get('order_by')
    order_direction = request.args.get('order_direction')

    return render_template('list.html',
                           questions=sorted_dict(questions, order_by, order_direction),
                           headers=QUESTION_HEADERS,
                           convert=datetime.utcfromtimestamp,
                           int=int,
                           sorted=sorted)


def sorted_dict(dict_, by=None, direction='asc'):
    """
    :param dict_:
        nested dictionary of questions or answers
    :param by:
        order parameter
    :param direction:
        asc or desc
    :return:
        same data structure as dict_, nested dictionary, ordered
    """
    ordered_dict = dict()
    if not by:
        by = 'submission_time'
    sorted_dict = sorted(dict_, key=lambda x: dict_[x][by], reverse=True if direction == 'desc' else False)
    for element in sorted_dict:
        ordered_dict.update({element: dict_[element]})
    return ordered_dict


@app.route('/question/<question_id>')
def display_question(question_id):
    questions = data_manager.get_questions()
    answers_for_question = util.get_answers_for_question_id(question_id, answers)

    return render_template('question.html', question_id=question_id, answers=answers_for_question, questions=questions, convert=datetime.utcfromtimestamp, int=int)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def new_answer(question_id):
    if request.method == 'POST':
        new_answer = dict()
        id = str(uuid.uuid4())
        new_answer['submission_time'] = round(datetime.now().timestamp() + 7200)
        new_answer['vote_number'] = 0
        new_answer['question_id'] = question_id
        new_answer['message'] = request.form.get('message')
        new_answer['image'] = None
        global answers
        answers.update({id: new_answer})
        connection.write_all_answers(answers)
        answers = data_manager.get_answers()
        return redirect(f'/question/{question_id}')
    else:
        return render_template('new_answer.html', question_id=question_id)


@app.route('/add-question', methods=['GET', 'POST'])
def new_question():
    if request.method == 'POST':
        new_question = dict()
        id = str(uuid.uuid4())

        new_question['id'] = id
        new_question['submission_time'] = round(datetime.now().timestamp() + 7200)
        new_question['view_number'] = 0
        new_question['vote_number'] = 0
        new_question['title'] = request.form.get('title')
        new_question['message'] = request.form.get('message')
        new_question['image'] = None

        global questions
        questions.update({id: new_question})
        connection.write_all_questions(questions)
        questions = data_manager.get_questions()
        return redirect('/')
    elif request.method == 'GET':
        return render_template('add_question.html')


@app.route('/question/<question_id>/vote-up', methods=['POST', 'GET'])
def vote_up(question_id):
    global questions
    questions[question_id]['vote_number'] += 1
    connection.write_all_questions(questions)
    return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>/vote-down', methods=['POST', 'GET'])
def vote_down(question_id):
    global questions
    questions[question_id]['vote_number'] -= 1
    connection.write_all_questions(questions)
    return redirect(f'/question/{question_id}')


if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=8000
    )