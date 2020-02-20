import connection, utility


@connection.connection_handler
def get_all_questions(cursor):
    cursor.execute("""SELECT * FROM question ORDER BY submission_time DESC;""")
    data = cursor.fetchall()
    return data


def get_latest_questions():
    list_latest_questions = []
    latest_questions = get_all_questions()
    if len(latest_questions) >= 5:
        for question in range(0, 5):
            list_latest_questions.append(latest_questions[question])
    else:
        for question in range(0, len(latest_questions)):
            list_latest_questions.append(latest_questions[question])
    return list_latest_questions


@connection.connection_handler
def get_all_question_comments(cursor):
    cursor.execute("""SELECT * FROM comment WHERE question_id IS NOT NULL;""")
    question_comments = cursor.fetchall()
    return question_comments


@connection.connection_handler
def get_all_answers_comments(cursor):
    cursor.execute("""SELECT * FROM comment WHERE answer_id IS NOT NULL;""")
    answer_comments = cursor.fetchall()
    return answer_comments


def get_question_comments(id):
    comments = get_all_question_comments()
    for comment in comments:
        if int(comment['question_id']) == int(id):
            return comment


def get_answer_comments(answer_id):
    comments_ans = get_all_answers_comments()
    for comment_for_answer in comments_ans:
        if int(comment_for_answer['answer_id']) == int(answer_id):
            return comment_for_answer


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
def update_question(cursor, table, title, message, question_id):
    cursor.execute(f"""UPDATE {table} SET title = '{title}', message = '{message}' WHERE id={question_id};""")


@connection.connection_handler
def update_answer(cursor, answer_id, message):
    cursor.execute(f"""UPDATE answer SET message = '{message}' WHERE id={answer_id};""")


@connection.connection_handler
def delete_row(cursor, table, identifier, question_id):
    cursor.execute(f"""DELETE FROM {table} WHERE {identifier} = {question_id}; """)


@connection.connection_handler
def get_comment(cursor, answer_id):
    cursor.execute("""SELECT * FROM comment WHERE answer_id=%(answer_id)s;""",
                   {'answer_id': answer_id}
                   )
    comment = cursor.fetchall()
    print(comment)
    return comment


@connection.connection_handler
def add_comment_ans(cursor, answer_id, message):
    id = utility.generate_comment_id()
    answer_id = answer_id
    message = message
    submission_time = utility.get_date()
    print(submission_time)
    edited_count = 0
    query = f"""INSERT INTO comment VALUES({id}, NULL, {answer_id}, '{message}', {edited_count}, '{submission_time}');"""
    cursor.execute(query)
    # comment_ans = cursor.fetchall()
    # return comment_ans


#
# @connection.connection_handler
# def get_all_comments_for_ans(id):
