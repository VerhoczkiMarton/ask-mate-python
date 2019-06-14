import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, session

import connection
import util
from util import sorted_dict

app = Flask(__name__)
app.secret_key = os.urandom(50)

QUESTION_HEADERS = ['Submission time', 'View number', 'Vote number', 'Title', 'Message', 'Image']
ANSWER_HEADERS = ['Submission time', 'Vote number', 'Question id', 'Message', 'Image']


@app.route('/')
def list_all():
    questions = connection.get_latest_5_questions()
    return render_template('index.html',
                           questions=questions,
                           headers=QUESTION_HEADERS)


@app.route('/list')
def list_last_5():
    questions = connection.get_all_from_table('question')
    order_by = request.args.get('order_by')
    order_direction = request.args.get('order_direction')

    return render_template('list.html',
                           questions=sorted_dict(questions, order_by, order_direction),
                           headers=QUESTION_HEADERS, order_by=order_by, order_direction=order_direction)


@app.route('/statistics/<int:question_id>')
def statistics(question_id):
    connection.view_question(question_id)
    return redirect(f'/question/{question_id}')


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
        new_question['image'] = request.form.get('image')
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


@app.route('/question/<int:question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == 'GET':
        question = connection.get_question_by_question_id(question_id)
        return render_template('edit_question.html', question=question, question_id=question_id)
    elif request.method == 'POST':
        message = request.form.get('message')
        title = request.form.get('title')
        image = request.form.get('image')
        connection.edit_question(question_id, message, title, image)
        return redirect(f'/question/{question_id}')


@app.route('/question/<int:question_id>/delete')
def delete_question(question_id):
    connection.delete_question(question_id)
    return redirect('/list')


@app.route('/answer/<int:answer_id>/edit', methods=['POST', 'GET'])
def edit_answer(answer_id):
    if request.method == 'GET':
        answer = connection.get_answer_by_id(answer_id)
        return render_template("edit_answer.html", answer_id=answer_id, answer_message=answer['message'])
    elif request.method == 'POST':
        edited_answer_message = request.form.get('message')
        connection.edit_answer(edited_answer_message, answer_id)
        question_id = connection.get_question_id_by_answer_id(answer_id)
        return redirect(f'/question/{question_id}')


@app.route('/answer/<int:answer_id>/delete')
def delete_answer(answer_id):
    question_id = connection.get_question_id_by_answer_id(answer_id)
    connection.delete_answer(answer_id)
    return redirect(f'/question/{question_id}')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        new_user = dict()
        new_user['username'] = request.form.get('username')
        new_user['hashed_password'], new_user['salt'] = util.hash_password(request.form.get('password'))
        new_user['registration_date'] = datetime.now()
        username_already_exists = connection.username_already_exists(new_user['username'])
        if username_already_exists:
            return render_template('register.html', username_already_exists=username_already_exists)
        else:
            connection.add_user(new_user)
            return redirect('/')
    elif request.method == 'GET':
        return render_template('register.html', username_already_exists=False)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html', invalid=False)
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        valid = connection.validate_password(username, password)
        if valid:
            session['active'] = True
            session['user'] = username
            return redirect('/')
        else:
            return render_template('login.html', invalid=True)


@app.route('/logout')
def logout():
    session.pop('active', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/list-users')
def list_all_users():
    all_users = connection.get_all_users()
    return render_template('all_users.html', all_users=all_users)


@app.route('/user/<username>')
def user_page(username):
    reg_date = connection.get_registration_date_by_username(username)
    return render_template('user_page.html', username=username, reg_date=reg_date)


@app.route('/search')
def search():
    term = request.args.get('term')
    filtered_questions = connection.search(term)
    order_by = request.args.get('order_by')
    order_direction = request.args.get('order_direction')
    return render_template('list.html',
                           questions=filtered_questions,
                           headers=QUESTION_HEADERS, order_by=order_by,
                           order_direction=order_direction,
                           term=term)

if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=8000
    )
