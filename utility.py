import connection
import server

# This function takes an integer as parameter
# Search for certain id question in dictionary
# Returns dictionary of values with whole question details

def display_question(question_id):
    dict_with_question = connection.read_from_csv("sample_data/question.csv")
    for row in dict_with_question:
        if row["id"] == question_id:
            return row

# This function takes a string as parameter
# It searches the maximum value of "ids" or "submission times"
# Returns an integer

def generate_value(type_of_value):
    dict_with_question = connection.read_from_csv("sample_data/question.csv")
    list_of_values = []
    for row in dict_with_question:
        list_of_values.append(int(row[type_of_value]))
    return max(list_of_values) + 1


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in server.ALLOWED_EXTENSIONS



