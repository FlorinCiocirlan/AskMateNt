from flask import Flask, request, redirect, render_template, url_for
import connection, data_manager, utility

app = Flask(__name__, template_folder="template", static_folder="static")


@app.route("/")
def index_route():
    return render_template("index.html")


@app.route("/list")
def list_route():
    dicti = connection.read_from_csv("sample_data/question.csv")
    fieldnames = ["Submission time", "View number", "Vote number", "Title"]
    return render_template("list.html", file=dicti, fieldnames=fieldnames)


@app.route("/question/int:<id>")
def question_route(id):
    question = utility.display_question(id)
    return render_template("question-page.html", to_display=question)

@app.route("/add-question", methods=["GET", "POST"])
def add_question_route():
    return redirect("list.html")

if __name__ == "__main__":
    app.run(debug=True,
            port=5000)
