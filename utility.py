import connection
import data_manager
from datetime import datetime


@connection.connection_handler
def generate_question_id(cursor):
    cursor.execute("""SELECT id FROM question;""")
    list_of_ids = []
    dict_with_ids = cursor.fetchall()
    for row in dict_with_ids:
        list_of_ids.append(int(row['id']))
    return max(list_of_ids) + 1


@connection.connection_handler
def generate_answer_id(cursor):
    cursor.execute("""SELECT id FROM answer;""")
    list_of_ids = []
    dict_with_ids = cursor.fetchall()
    for row in dict_with_ids:
        list_of_ids.append(int(row['id']))
    return max(list_of_ids) + 1


@connection.connection_handler
def generate_comment_id(cursor):
    cursor.execute("""SELECT id FROM comment ORDER BY id DESC;""")
    current_max = cursor.fetchone()
    return current_max['id'] + 1


@connection.connection_handler
def sort_question(cursor, sortby, direction):
    if "time" in sortby:
        sortby = "submission" + "_time"
    elif sortby == "votes":
        sortby = sortby.rstrip("s").lower() + "_number"
    elif sortby == "views":
        sortby = sortby.rstrip("s").lower() + "_number"

    cursor.execute(
        """SELECT * from question ORDER BY {sortby} {direction};""".format(sortby=sortby, direction=direction))
    sorted_question = cursor.fetchall()
    return sorted_question


def get_date():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")



@connection.connection_handler
def get_comments(cursor, answer_id):
    query = """SELECT * from comment
                WHERE answer_id=%(answer_id)s;"""
    data = {
        "answer_id": answer_id
    }
    cursor.execute(query, data)
    return cursor.fetchall()

