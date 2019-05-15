from csv import DictReader, DictWriter

def get_all_answers():
    all_answers = []
    input_file = DictReader(open("answers.csv"))
    for line in input_file:
        all_answers.append(line)
    return all_answers


def get_all_questions():
    all_questions = []
    input_file = DictReader(open("questions.csv"))
    for line in input_file:
        all_questions.append(line)
    return all_questions


def write_all_questions(questions):
    fieldnames = get_headers('questions')
    with open('questions.csv', 'w') as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for question in questions.values():
            writer.writerow(question)


def write_all_answers(answers):
    fieldnames = get_headers('answers')
    with open('answers.csv', 'w') as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for id, answer in answers.items():
            answer['id'] = id
            writer.writerow(answer)


def get_headers(file):
    with open(f'{file}.csv', 'r') as f:
        headers = f.readline().strip().split(',')
    return headers
