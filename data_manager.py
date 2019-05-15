import connection


def get_answers():
    list_of_all_answers = connection.get_all_answers()
    answers = dict()
    for answer in list_of_all_answers:
        id = answer.pop('id')
        answer = parse_all_ints(answer)
        answers.update({id: answer})
    return answers


def get_questions():
    list_of_all_questions = connection.get_all_questions()
    questions = dict()
    for question in list_of_all_questions:
        id = question.pop('id')
        question = parse_all_ints(question)
        questions.update({id: question})
    return questions


def parse_all_ints(dict_):
    for key, value in dict_.items():
        try:
            dict_[key] = int(value)
        except ValueError:
            continue
    return dict_
