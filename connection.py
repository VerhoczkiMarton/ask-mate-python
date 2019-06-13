import connection_common
import data_manager
import util


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
        """, {'id': question['id'], 'submission_time': question['submission_time'],
              'view_number': question['view_number'], 'vote_number': question['vote_number'],
              'title': question['title'], 'message': question['message'], 'image': question['image']})


@connection_common.connection_handler
def new_answer(cursor, answer):
    cursor.execute("""
    INSERT INTO answer 
    VALUES (%(id)s, %(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s)
    """, {'id': answer['id'], 'submission_time': answer['submission_time'], 'vote_number': answer['vote_number'],
          'question_id': answer['question_id'], 'message': answer['message'], 'image': answer['image']})


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
def edit_answer(cursor, edited_answer_message, answer_id):
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
    """, {'answer_id': answer_id})
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
def edit_question(cursor, question_id, message, title, image):
    cursor.execute("""
    UPDATE question
    SET  title = %(title)s, message = %(message)s, image = %(image)s
    WHERE id = %(id)s
                   """, {'id': question_id, 'title': title, 'message': message, 'image': image})


@connection_common.connection_handler
def delete_question(cursor, question_id):
    cursor.execute(""" 
    DELETE FROM question
    WHERE id = %(question_id)s;
    """, {'question_id': question_id})


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
    DELETE from answer
    WHERE id = %(answer_id)s;
    """, {'answer_id': answer_id})


@connection_common.connection_handler
def add_user(cursor, new_user):
    cursor.execute("""
    INSERT INTO users
    VALUES (%(username)s, %(salt)s, %(password)s, %(registration_date)s)
    """, {'username': new_user['username'],
          'password': new_user['hashed_password'],
          'salt': new_user['salt'],
          'registration_date': new_user['registration_date']})


@connection_common.connection_handler
def username_already_exists(cursor, username):
    cursor.execute("""
    SELECT username FROM users
    WHERE username ILIKE %(username)s
    """, {'username': username})
    query_to_test = cursor.fetchone()
    if query_to_test:
        return True
    else:
        return False


@connection_common.connection_handler
def validate_password(cursor, username, password):
    cursor.execute("""
    SELECT salt, password, username
    FROM users
    WHERE username = %(username)s
    """, {'username': username})
    try:
        db_credentials = cursor.fetchall()[0]
    except BaseException:
        return False
    auth_string = db_credentials['username'] + db_credentials['password']

    user_auth_string = username + util.hash_password_with_custom_salt(password, db_credentials['salt'])
    if auth_string == user_auth_string:
        return True
    else:
        return False


@connection_common.connection_handler
def get_all_users(cursor):
    cursor.execute("""
    SELECT username, registration_date
    FROM users
    """)
    return cursor.fetchall()


@connection_common.connection_handler
def view_question(cursor, question_id):
    cursor.execute("""
    UPDATE question
    SET view_number = view_number + 1
    WHERE question.id = %(question_id)s
    """, {'question_id': question_id})


@connection_common.connection_handler
def get_registration_date_by_username(cursor, username):
    cursor.execute("""
                SELECT registration_date FROM users
                WHERE username = %(username)s
                """, {"username": username})
    reg_date = cursor.fetchall()[0]
    return reg_date['registration_date']
