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




def get_date():
    return datetime.now().strftime("%Y-%d-%m %H:%M:%S")





