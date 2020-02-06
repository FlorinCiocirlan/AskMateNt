import connection, utility


@connection.connection_handler
def get_all_questions(cursor):
    cursor.execute("""SELECT * FROM question;""")
    data = cursor.fetchall()
    return data


#  @connection.connection_handler
# def get_all_answers(cursor):
#     cursor.execute("""SELECT * FROM answer;""")
#     data = cursor.fetchall()
#     return data
#

@connection.connection_handler
def add_question(cursor, title, message):
    id = utility.generate_question_id()
    submission_time = utility.get_date()
    view_number = 0
    vote_number = 0
    title = title
    message = message
    image = ''

    cursor.execute(
        """INSERT INTO question VALUES('{id}','{submission_time}', '{view_number}', '{vote_number}', '{title}', '{message}', '{image}');""".format(
            id=id, submission_time=submission_time, view_number=view_number, vote_number=vote_number, title=title,
            message=message, image=image
        ))


@connection.connection_handler
def add_answers(cursor, question_id, message):
    id = utility.generate_answer_id()
    submission_time = utility.get_date()
    vote_number = 0
    message = message
    image = ''
    question_id = question_id
    cursor.execute(
        """INSERT INTO answer VALUES('{id}','{submission_time}', '{vote_number}', '{question_id}', '{message}', '{image}');""".format(
            id=id, submission_time=submission_time, vote_number=vote_number, question_id=question_id, message=message,
            image=image
        ))


@connection.connection_handler
def get_question(cursor, question_id):
    cursor.execute("""SELECT * FROM question WHERE id=%(id)s;""",
                   {"id": question_id}
                   )

    question = cursor.fetchone()
    return question


@connection.connection_handler
def get_all_answers(cursor, question_id):
    cursor.execute("""SELECT * FROM answer WHERE question_id=%(question_id)s;""",
                   {"question_id": question_id}
                   )

    answer = cursor.fetchall()
    return answer


@connection.connection_handler
def update_data(cursor, table, title, message, question_id):
    cursor.execute(f"""UPDATE {table} SET title = '{title}', message = '{message}' WHERE id={question_id};""")

@connection.connection_handler
def delete_row(cursor, table, identifier, question_id):
    cursor.execute(f"""DELETE FROM {table} WHERE {identifier} = {question_id}; """)
