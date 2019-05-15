import datetime


def get_answers_for_question_id(question_id, answers):
    answers_for_question_id = []
    for answer in answers.values():
        if answer['question_id'] == int(question_id):
            answers_for_question_id.append(answer)
    return answers_for_question_id


def convert_timestamp(questions, answers):
    for record in questions.values():
        record['submission_time'] = datetime.datetime.utcfromtimestamp(float(record['submission_time'])).strftime('%Y-%m-%d %H:%M')

    for record in answers.values():
        record['submission_time'] = datetime.datetime.utcfromtimestamp(float(record['submission_time'])).strftime('%Y-%m-%d %H:%M')
