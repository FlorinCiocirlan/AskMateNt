from flask import Flask, request, redirect, render_template, url_for
import connection, data_manager, utility
import os, sys
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/images'

app = Flask(__name__, template_folder="template", static_folder="static", )
app.config['UPLOAD_FOLDER'] = "static/images/"


@app.route("/")
def index_route():
    return render_template("index.html")


@app.route("/list")
def list_route():
    dicti = connection.read_from_csv("sample_data/question.csv")
    fieldnames = ["Submission time", "View number", "Vote number", "Title"]
    return render_template("list.html", file=dicti, fieldnames=fieldnames)


@app.route("/question/<id>")
def question_route(id):
    question = utility.display_question(id)
    return render_template("question-page.html", to_display=question)


@app.route("/add-question", methods=["GET", "POST"])
def add_question_route():
    if request.method == "POST":
        id = utility.generate_value("id")
        submission_time = utility.generate_submission()
        view_number = 0
        vote_number = 0
        title = request.form["title"]
        message = request.form["message"]

        if request.files["picture"]:
            f = request.files['picture']
            image = f.filename
            f.save(app.config['UPLOAD_FOLDER'] + secure_filename(f.filename))

        list_to_write = [id, submission_time, view_number, vote_number, title, message, image]
        connection.append_to_csv("sample_data/question.csv", list_to_write)

        return redirect("list")
    return render_template("add-question.html")


if __name__ == "__main__":
    app.run(debug=True,
            port=5000)
