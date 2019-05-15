import datetime


def get_answers_for_question_id(question_id, answers):
    answers_for_question_id = []
    for answer in answers.values():
        if str(answer['question_id']) == question_id:
            answers_for_question_id.append(answer)
    return answers_for_question_id
