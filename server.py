from flask import Flask, render_template, request, redirect, url_for
import connection
import util
import uuid
from datetime import datetime

app = Flask(__name__)

QUESTION_HEADERS = ['Submission time', 'View number', 'Vote number', 'Title', 'Message', 'Image']
ANSWER_HEADERS = ['Submission time', 'Vote number', 'Question id', 'Message', 'Image']

@app.route('/')
@app.route('/list')
def route_list():
    questions = connection.get_all_from_table('question')
    order_by = request.args.get('order_by')
    order_direction = request.args.get('order_direction')

    return render_template('list.html',
                           questions=sorted_dict(questions, order_by, order_direction),
                           headers=QUESTION_HEADERS)


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


@app.route('/question/<int:question_id>')
def display_question(question_id):
    questions = connection.get_all_from_table('question')
    answers_for_question = connection.get_answers_for_question_id(question_id)

    return render_template('question.html',
                           question_id=question_id,
                           answers=answers_for_question,
                           questions=questions)


@app.route('/question/<int:question_id>/new-answer', methods=['GET', 'POST'])
def new_answer(question_id):
    if request.method == 'POST':
        new_answer = dict()
        new_answer['id'] = connection.get_answer_id()
        new_answer['submission_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_answer['vote_number'] = 0
        new_answer['question_id'] = question_id
        new_answer['message'] = request.form.get('message')
        new_answer['image'] = None

        connection.new_answer(new_answer)

        return redirect(f'/question/{question_id}')
    else:
        return render_template('new_answer.html', question_id=question_id)


@app.route('/add-question', methods=['GET', 'POST'])
def new_question():
    if request.method == 'POST':
        new_question = dict()
        id = connection.get_question_id()

        new_question['id'] = id
        new_question['submission_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_question['view_number'] = 0
        new_question['vote_number'] = 0
        new_question['title'] = request.form.get('title')
        new_question['message'] = request.form.get('message')
        new_question['image'] = None
        connection.new_question(new_question)
        return redirect('/')
    elif request.method == 'GET':
        return render_template('add_question.html')


@app.route('/question/<int:question_id>/vote-up', methods=['POST', 'GET'])
def vote_up(question_id):
    connection.vote_up(question_id)
    return redirect(f'/question/{question_id}')


@app.route('/question/<int:question_id>/vote-down', methods=['POST', 'GET'])
def vote_down(question_id):
    connection.vote_down(question_id)
    return redirect(f'/question/{question_id}')


if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=8000
    )