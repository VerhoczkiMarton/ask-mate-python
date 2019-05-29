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
    cursor.execute("""
        INSERT INTO question 
        VALUES (%(id)s, %(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s)
        """, {'id': question['id'], 'submission_time': question['submission_time'], 'view_number': question['view_number'], 'vote_number': question['vote_number'],
              'title': question['title'], 'message': question['message'], 'image': question['image']})


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


@connection_common.connection_handler
def vote_up(cursor, question_id):
    cursor.execute("""
    UPDATE question
    SET vote_number=vote_number+1
    WHERE id=%(question_id)s
                   """, {'question_id': question_id})


@connection_common.connection_handler
def vote_down(cursor, question_id):
    cursor.execute("""
    UPDATE question
    SET vote_number=vote_number-1
    WHERE id=%(question_id)s
                   """, {'question_id': question_id})


@connection_common.connection_handler
def edit_answer(cursor,edited_answer_message, answer_id):
    cursor.execute("""
    UPDATE answer
    SET message = %(edited_answer_message)s
    WHERE id = %(answer_id)s
    """, {'edited_answer_message': edited_answer_message, 'answer_id': answer_id})


@connection_common.connection_handler
def get_question_id_by_answer_id(cursor, answer_id):
    cursor.execute("""
    SELECT question_id FROM answer
    WHERE id = %(answer_id)s
    """, {'answer_id':answer_id})
    return cursor.fetchone()['question_id']


@connection_common.connection_handler
def get_answer_by_id(cursor, answer_id):
    cursor.execute("""
    SELECT * FROM answer
    WHERE id = %(answer_id)s
    """, {'answer_id': answer_id})
    return cursor.fetchone()


@connection_common.connection_handler
def get_question_by_question_id(cursor, question_id):
    cursor.execute("""
    SELECT  * FROM question
    WHERE id = %(question_id)s
    """, {'question_id': question_id})
    return cursor.fetchone()


@connection_common.connection_handler
def edit_question(cursor, question_id, message, title):
    cursor.execute("""
    UPDATE question
    SET  title = %(title)s, message = %(message)s
    WHERE id = %(id)s
                   """, {'id': question_id, 'title': title, 'message': message})


@connection_common.connection_handler
def delete_question(cursor, question_id):
    cursor.execute("""
    DELETE FROM question
    WHERE id = %(id)s
    """, {'id': question_id})


@connection_common.connection_handler
def get_latest_5_questions(cursor):
    cursor.execute("""
    SELECT *
    FROM question
    ORDER BY submission_time DESC 
    LIMIT 5
    """)
    return data_manager.convert_data_structure(cursor.fetchall())


@connection_common.connection_handler
def delete_answer(cursor, answer_id):
    cursor.execute("""
    DELETE FROM comment
    WHERE answer_id = %(answer_id)s;
    
    DELETE from answer
    WHERE id = %(answer_id)s;
    """, {'answer_id': answer_id})
