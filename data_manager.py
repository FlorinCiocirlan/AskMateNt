import connection, utility


@connection.connection_handler
def get_all_questions(cursor):
    cursor.execute("""SELECT * FROM question ORDER BY submission_time DESC;""")
    data = cursor.fetchall()
    return data

def question_search_result(search_phrase):
    splited_search_phrase=search_phrase.split()
    all_questions = get_all_questions()

    for word in list(splited_search_phrase):
        print(word, splited_search_phrase, word)
        if len(word) < 3:
            splited_search_phrase.remove(word)

    questions_keyword_list = []
    for question in all_questions:
        if any( word.lower() in question['title'].lower() or word in question['message'].lower() for word in splited_search_phrase ):
            questions_keyword_list.append(question)
    return questions_keyword_list

def answer_search_result(search_phrase):
    all_answers=get_every_answer()
    answers_keyword_list = []
    for answer in all_answers:
        if search_phrase in answer['message']:
            answers_keyword_list.append(answer)
    return answers_keyword_list

def get_latest_questions():
    list_latest_questions = []
    latest_questions = get_all_questions()
    if len(latest_questions) >= 5:
        for question in range(0,5):
            list_latest_questions.append(latest_questions[question])
    else:
        for question in range(0,len(latest_questions)):
            list_latest_questions.append(latest_questions[question])
    return list_latest_questions


@connection.connection_handler
def get_all_question_comments(cursor):
    cursor.execute("""SELECT * FROM comment WHERE question_id IS NOT NULL;""")
    question_comments=cursor.fetchall()
    return question_comments

def get_question_comments(id):
    comments = get_all_question_comments()
    list_with_comments = [comment for comment in comments if int(comment['question_id']) == int(id)]
    return list_with_comments

def get_comment(question_id, comment_id):
    question_comments = get_question_comments(question_id)
    for comment in question_comments:
        if int(comment['id']) == int(comment_id):
            return comment

def get_questionId_by_commentId(comment_id):
    all_comments = get_all_question_comments()
    for comment in all_comments:
        if int(comment['id']) == int(comment_id):
            return comment['question_id']

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
def vote_question_up(cursor, question_id):
    question = get_question(question_id)
    new_vote = question['vote_number'] + 1
    cursor.execute(f"""UPDATE question SET vote_number = {new_vote} WHERE id={question_id}""")

@connection.connection_handler
def vote_question_down(cursor, question_id):
    question = get_question(question_id)
    new_vote = question['vote_number'] - 1
    cursor.execute(f"""UPDATE question SET vote_number = {new_vote} WHERE id={question_id}""")


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


@connection.connection_handler
def update_question(cursor, table, title, message, question_id):
    cursor.execute(f"""UPDATE {table} SET title = '{title}', message = '{message}' WHERE id={question_id};""")

@connection.connection_handler
def update_answer(cursor, answer_id, message):
    cursor.execute(f"""UPDATE answer SET message = '{message}' WHERE id={answer_id};""")

@connection.connection_handler
def delete_row(cursor, table, column, id):
    cursor.execute(f"""DELETE FROM {table} WHERE {column} = {id}; """)


@connection.connection_handler
def update_comment(cursor, edited_comment, comment_id):
    new_date = utility.get_date()
    edited_count = update_edited_count(comment_id)
    cursor.execute(f"""UPDATE comment SET message = '{edited_comment}', edited_count = '{edited_count}', submission_time = '{new_date}' WHERE id='{comment_id}';""")

def update_edited_count(comment_id):
    comments = get_all_question_comments()
    for comment in comments:
        if int(comment['id']) == int(comment_id):
            edited_count = comment['edited_count']
    if edited_count:
        return edited_count + 1
    else:
        return 1


@connection.connection_handler
def add_question_comment(cursor, question_id,message):
    id = utility.generate_comment_id()
    question_id=question_id
    message=message
    submission_time=utility.get_date()
    cursor.execute(f"""INSERT INTO comment VALUES('{id}', '{question_id}', NULL, '{message}', '{submission_time}');""")



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

