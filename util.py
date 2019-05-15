
def get_answers_for_question_id(question_id, answers):
    answers_for_question_id = []
    for answer in answers.values():
        if answer['question_id'] == int(question_id):
            answers_for_question_id.append(answer)
    return answers_for_question_id
