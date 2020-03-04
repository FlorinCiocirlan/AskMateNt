import connection, utility
from psycopg2 import sql

################# Questions functions ##############################


@connection.connection_handler
def get_question(cursor, question_id):
    cursor.execute("""SELECT * FROM question WHERE id=%(id)s;""",
                   {"id": question_id}
                   )
    question = cursor.fetchone()
    return question

@connection.connection_handler
def vote_question_down(cursor, question_id):
    question = get_question(question_id)
    new_vote = question['vote_number'] - 1
    cursor.execute(f"""UPDATE question SET vote_number = {new_vote} WHERE id={question_id}""")


@connection.connection_handler
def vote_question_up(cursor, question_id):
    question = get_question(question_id)
    new_vote = question['vote_number'] + 1
    cursor.execute(f"""UPDATE question SET vote_number = {new_vote} WHERE id={question_id}""")

@connection.connection_handler
def update_question(cursor, table, title, message, question_id):
    cursor.execute(
        sql.SQL("UPDATE {table} SET {title} = %s, {message} = %s WHERE {id}=%s;")
        .format(table=sql.Identifier(table),title=sql.Identifier('title'),message=sql.Identifier('message'),id=sql.Identifier('id')),
        [title, message, question_id]

        )

@connection.connection_handler
def add_question_comment(cursor, question_id,message,user_id):
    id = utility.generate_comment_id()
    question_id=question_id
    message=message
    edited_count = 0
    submission_time=utility.get_date()
    cursor.execute(
        sql.SQL("INSERT INTO {table} VALUES(%s, %s,NULL,%s,%s,%s,%s);")
            .format(table=sql.Identifier('comment')),
            [id, question_id, message,submission_time, edited_count,user_id]
    )


def get_comment(question_id, comment_id):
    question_comments = get_question_comments(question_id)
    for comment in question_comments:
        if int(comment['id']) == int(comment_id):
            return comment



def get_question_comments(id):
    comments = get_all_question_comments()
    list_with_comments = [comment for comment in comments if int(comment['question_id']) == int(id)]
    return list_with_comments

@connection.connection_handler
def add_question(cursor, title, message,user_id):
    id = utility.generate_question_id()
    submission_time = utility.get_date()
    view_number = 0
    vote_number = 0
    title = title
    message = message
    image = ''
    cursor.execute(
        sql.SQL("INSERT INTO {table} VALUES(%s, %s, %s,%s,%s,%s,%s,%s);")
        .format(table=sql.Identifier('question')),
        [id, submission_time, view_number, vote_number, title, message, image,user_id]
    )




def get_questionId_by_commentId(comment_id):
    all_comments = get_all_question_comments()
    for comment in all_comments:
        if int(comment['id']) == int(comment_id):
            return comment['question_id']


def get_questionID_by_answerId(answer_id):
    all_answers=get_every_answer()
    for answer in all_answers:
        if int(answer['id']) == int(answer_id):
            return answer['question_id']

def get_answerId_by_questionId(question_id):
    all_answers=get_every_answer()
    for answer in all_answers:
        if int(answer['question_id']) == int(question_id):
            return answer['id']



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
def get_all_questions(cursor):
    cursor.execute("""SELECT * FROM question ORDER BY submission_time DESC;""")
    data = cursor.fetchall()
    return data


def question_search_result(search_phrase):
    splitted_search_phrase=search_phrase.split()
    all_questions = get_all_questions()

    for word in list(splitted_search_phrase):
        if len(word) < 3:
            splitted_search_phrase.remove(word)

    questions_keyword_list = []
    for question in all_questions:
        if any( word.lower() in question['title'].lower() or word in question['message'].lower() for word in splitted_search_phrase ):
            questions_keyword_list.append(question)
    return questions_keyword_list

################## Answers functions ########################
@connection.connection_handler
def vote_answer_up(cursor, answer_id):
    answer = get_answer(answer_id)
    new_vote = answer['vote_number'] + 1
    cursor.execute(f"""UPDATE answer SET vote_number = {new_vote} WHERE id={answer_id}""")
@connection.connection_handler
def vote_answer_down(cursor, answer_id):
    answer = get_answer(answer_id)
    new_vote = answer['vote_number'] - 1
    cursor.execute(f"""UPDATE answer SET vote_number = {new_vote} WHERE id={answer_id}""")


def answer_search_result(search_phrase):
    splitted_search_phrase=search_phrase.split()
    all_answers=get_every_answer()

    for word in list(splitted_search_phrase):
        if len(word) < 3:
            splitted_search_phrase.remove(word)

    answers_keyword_list = []
    for answer in all_answers:
        if any(word in answer['message'].lower() for word in splitted_search_phrase):
            answers_keyword_list.append(answer)
    return answers_keyword_list




@connection.connection_handler
def add_answers(cursor, question_id, message,user_id):
    id = utility.generate_answer_id()
    submission_time = utility.get_date()
    vote_number = 0
    question_id = question_id
    message = message
    image = ''
    cursor.execute(
        sql.SQL("INSERT INTO {table} VALUES(%s, %s, %s, %s, %s, %s, %s);")
            .format(table=sql.Identifier('answer')),
            [id, submission_time, vote_number, question_id, message, image,user_id]
        )



@connection.connection_handler
def get_all_answers(cursor, question_id):
    cursor.execute("""SELECT * FROM answer WHERE question_id=%(question_id)s;""",
                   {"question_id": question_id}
                   )
    answer = cursor.fetchall()
    return answer


@connection.connection_handler
def get_every_answer(cursor):
    cursor.execute("""SELECT * FROM answer""")
    answers = cursor.fetchall()
    return answers

def get_answerId_by_commentId(comment_id):
    all_comments = get_all_answers_comments()
    for comment in all_comments:
        if int(comment['id']) == int(comment_id):
            return comment['answer_id']


def get_answer(answer_id):
    answers=get_every_answer()
    for answer in answers:
        if int(answer['id']) == int(answer_id):
            return answer

########################### General functions #######################



@connection.connection_handler
def update_answer(cursor, answer_id, message):
    cursor.execute(
        sql.SQL("UPDATE {table} SET {message} = %s WHERE {id}=%s;")
        .format(table=sql.Identifier('answer'),message=sql.Identifier('message'),id=sql.Identifier('id')),
        [message,answer_id]
    )


@connection.connection_handler
def delete_row(cursor, table, column, id):
    cursor.execute(
        sql.SQL("DELETE FROM {table} WHERE {column} = %s;")
        .format(table=sql.Identifier(table), column=sql.Identifier(column)),
        [id]
    )


########################## Comments functions ###########################
@connection.connection_handler
def update_edited_count(cursor,comment_id):
    cursor.execute(
        sql.SQL("UPDATE comment SET {edited_count}={edited_count} + 1 WHERE {id} = %s;")
        .format(id=sql.Identifier('id'), edited_count=sql.Identifier('edited_count')),
        [comment_id]
    )


@connection.connection_handler
def update_comment(cursor, edited_comment, comment_id):
    new_date = utility.get_date()
    cursor.execute(
        sql.SQL("UPDATE comment SET {message} = %s, {submission_time} = %s WHERE {id}=%s;")
        .format(message=sql.Identifier('message'), submission_time=sql.Identifier('submission_time'), id=sql.Identifier('id')),
        [edited_comment, new_date, comment_id]
    )

@connection.connection_handler
def add_comment_ans(cursor, answer_id, message, user_id):
    id = utility.generate_comment_id()
    answer_id = answer_id
    message = message
    submission_time = utility.get_date()
    edited_count = 0
    user_id=session['user_id']
    cursor.execute(
        sql.SQL("INSERT INTO comment VALUES(%s , NULL,  %s , %s, %s, %s, %s);"),
        [id, answer_id, message, submission_time, edited_count, user_id]
    )



def get_answer_comment(comment_id):
    comments = get_all_answers_comments()
    for comment in comments:
        if int(comment['id']) == int(comment_id):
            return comment


@connection.connection_handler
def get_all_answers_comments(cursor):
    cursor.execute("""SELECT * FROM comment WHERE answer_id IS NOT NULL;""")
    answer_comments = cursor.fetchall()
    return answer_comments

def get_certain_answer_comments(answer_id):
    answer_comments = get_all_answers_comments()
    answer_comments_list =[]
    for comment in answer_comments:
        if int(comment['answer_id']) == int(answer_id):
            answer_comments_list.append(comment)
    return answer_comments_list


@connection.connection_handler
def get_all_question_comments(cursor):
    cursor.execute("""SELECT * FROM comment WHERE question_id IS NOT NULL;""")
    question_comments = cursor.fetchall()
    return question_comments


def get_questionID_by_answerId(answer_id):
    all_answers=get_every_answer()
    for answer in all_answers:
        if int(answer['id']) == int(answer_id):
            return answer['question_id']

@connection.connection_handler
def vote_answer_up(cursor, answer_id):
    answer = get_answer(answer_id)
    new_vote = answer['vote_number'] + 1
    cursor.execute(f"""UPDATE answer SET vote_number = {new_vote} WHERE id={answer_id}""")

@connection.connection_handler
def vote_answer_down(cursor, answer_id):
    answer = get_answer(answer_id)
    new_vote = answer['vote_number'] - 1
    cursor.execute(f"""UPDATE answer SET vote_number = {new_vote} WHERE id={answer_id}""")
    
############### User Management ###################
@connection.connection_handler
def insert_user(cursor,username,password,email):
    creation_date = utility.get_date()
    id=utility.generate_user_id()
    reputation = 0
    query=sql.SQL("INSERT INTO {table} VALUES(%s, %s, %s, %s, %s, %s );").format(table=sql.Identifier('users'))
    cursor.execute(query,[id,password,email,creation_date,reputation,username,])

@connection.connection_handler
def if_already_exist(cursor,column,data):
    query=sql.SQL("SELECT * FROM users")
    cursor.execute(query)
    new_data=cursor.fetchall()
    for row in new_data:
        if row[column] == data:
            return True

    return False

@connection.connection_handler
def get_hashed_password(cursor,username):
    query=sql.SQL("SELECT * FROM {table} WHERE {column} = %s;").format(table=sql.Identifier('users'), column=sql.Identifier('username'))
    cursor.execute(query,[username])
    password = cursor.fetchone()
    return password['password']

@connection.connection_handler
def find_id_by_username(cursor,username):
    query=sql.SQL("SELECT id FROM users WHERE username=%s")
    cursor.execute(query,[username])
    id = cursor.fetchone()
    return id['id']

