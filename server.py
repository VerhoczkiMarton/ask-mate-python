from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/list')
def route_list():
    pass


@app.route('/question/<question_id>')
def display_question(question_id):
    pass


@app.route('/add-question')
def add_question():
    pass


if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=8000
    )