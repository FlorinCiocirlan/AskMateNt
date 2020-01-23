import connection
import datetime
import time

# This function takes an integer as parameter
# Search for certain id question in dictionary
# Returns dictionary of values with whole question details

def display_question(question_id):
    dict_with_question = connection.read_from_csv("sample_data/question.csv")
    for row in dict_with_question:
        if row["id"] == question_id:
            return row


def display_answer(question_id):
    dict_with_question = connection.read_from_csv("sample_data/answer.csv")
    answers_list = []
    for row in dict_with_question:
        if row["question_id"] == question_id:
            answers_list.append(row)
    return answers_list



# This function takes a string as parameter
# It searches the maximum value of "ids" or "submission times"
# Returns an integer

def generate_value(type_of_value, file):
    dict_with_question = connection.read_from_csv(file)
    list_of_values = []
    for row in dict_with_question:
        list_of_values.append(int(row[type_of_value]))
    return max(list_of_values) + 1


def generate_submission():
    return str(int(time.time()))


def get_date(time_stamp):
    return time.strftime("%a, %d %B %Y %H:%M:%S",time.localtime(int(time_stamp)))





