from csv import DictReader, DictWriter

def get_all_answers():
    """
     Returns a list of all the answers
    """
    all_answers = []
    input_file = DictReader(open("answers.csv"))
    for line in input_file:
        all_answers.append(line)
    return all_answers


def get_all_questions():
    """
     Returns a list of all the questions
    """
    all_questions = []
    input_file = DictReader(open("questions.csv"))
    for line in input_file:
        all_questions.append(line)
    return all_questions


def write_all_questions(questions):
    """
    Writes the content of questions to the questions.csv file
    """
    fieldnames = get_headers('questions')
    questions_list = []
    for id, content in questions.items():
        temp_dict = dict(content.items())
        temp_dict.update({'id': id})
        questions_list.append(temp_dict)

    with open('questions.csv', 'w') as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for question in questions_list:
            writer.writerow(question)


def write_all_answers(answers):
    """
    Writes the content of answers to the answers.csv file
    """
    fieldnames = get_headers('answers')
    answers_list = []
    for id, content in answers.items():
        temp_dict = dict(content.items())
        temp_dict.update({'id': id})
        answers_list.append(temp_dict)
    with open('answers.csv', 'w') as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for answer in answers_list:
            writer.writerow(answer)


def get_headers(file):
    """
    Returns a list of all headers from file
    :param file:
    -answers
    -questions
    """
    with open(f'{file}.csv', 'r') as f:
        headers = f.readline().strip().split(',')
    return headers
