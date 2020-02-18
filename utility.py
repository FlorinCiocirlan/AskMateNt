from datetime import datetime
import connection

# This function takes a string as parameter
# It searches the maximum value of "ids" or "submission times"
# Returns an integer

@connection.connection_handler
def generate_question_id(cursor,):
    cursor.execute("""SELECT id FROM question;""")
    list_of_ids = []
    dict_with_ids = cursor.fetchall()
    for row in dict_with_ids:
        list_of_ids.append(int(row['id']))
    return max(list_of_ids) + 1

@connection.connection_handler
def generate_answer_id(cursor,):
    cursor.execute("""SELECT id FROM answer;""")
    list_of_ids = []
    dict_with_ids = cursor.fetchall()
    for row in dict_with_ids:
        list_of_ids.append(int(row['id']))
    return max(list_of_ids) + 1

@connection.connection_handler
def generate_comment_id(cursor):
    cursor.execute("""SELECT id FROM comment;""")
    list_of_ids = []
    dict_with_ids = cursor.fetchall()
    for row in dict_with_ids:
        list_of_ids.append(int(row['id']))
    return len(list_of_ids) + 1


@connection.connection_handler
def sort_question(cursor, sortby, direction):
    if "time" in sortby:
        sortby = "submission" + "_time"
    elif sortby == "votes":
        sortby = sortby.rstrip("s").lower() + "_number"
    elif sortby == "views":
        sortby = sortby.rstrip("s").lower() + "_numbers"

    cursor.execute("""SELECT * from question ORDER BY {sortby} {direction};""".format(sortby=sortby, direction=direction))
    sorted_question = cursor.fetchall()
    return sorted_question



def get_date():
    datetime.now().strftime("%Y-%M-%D %H:%M:%S")






