import connection
import server

def display_question(question_id):
    dict_with_question = connection.read_from_csv("sample_data/question.csv")
    for row in dict_with_question:
        if row["id"] == question_id:
            return row
