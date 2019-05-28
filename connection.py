import connection_common
import data_manager


@connection_common.connection_handler
def get_all_from_table(cursor, table):
    query = "SELECT * FROM " + table
    cursor.execute(query)
    return data_manager.convert_data_structure(cursor.fetchall())


@connection_common.connection_handler
def get_answers_for_question_id(cursor, question_id):
    cursor.execute("""
    SELECT * FROM answer
    WHERE question_id = %(question_id)s
    """, {'question_id': question_id})
    return data_manager.convert_data_structure(cursor.fetchall())


@connection_common.connection_handler
def new_question(cursor, question):
    pass

@connection_common.connection_handler
def new_answer(cursor, answer):
    cursor.execute("""
    INSERT INTO answer 
    VALUES (%(id)s, %(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s)
    """, {'id': answer['id'], 'submission_time': answer['submission_time'], 'vote_number': answer['vote_number'], 'question_id': answer['question_id'], 'message': answer['message'], 'image': answer['image']})


@connection_common.connection_handler
def get_answer_id(cursor):
    cursor.execute("""
    SELECT MAX(id) + 1 AS id
    FROM answer
    """)
    return cursor.fetchall()[0]['id']


@connection_common.connection_handler
def get_question_id(cursor):
    cursor.execute("""
    SELECT MAX(id) + 1 AS id
    FROM question
    """)
    return cursor.fetchall()[0]['id']
