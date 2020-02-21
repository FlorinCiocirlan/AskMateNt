from flask import Flask, request, redirect, render_template, url_for
import connection, data_manager, utility
import os, sys
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/images'

app = Flask(__name__, template_folder="template", static_folder="static")
app.config['UPLOAD_FOLDER'] = "static/images/"


@app.route("/")
def index_route():
    list_latest_questions = data_manager.get_latest_questions()
    fieldnames = ["Submission time", "View number", "Vote number", "Title"]
    return render_template("index.html", latest_questions=list_latest_questions, headers=fieldnames)


@app.route("/list", methods=["GET", "POST"])
def list_route():
    if request.method == "GET":
        questions = data_manager.get_all_questions()
        fieldnames = ["Submission time", "View number", "Vote number", "Title"]
        return render_template("list.html", file=questions, fieldnames=fieldnames)
    elif request.method == "POST":
        fieldnames = ["Submission time", "View number", "Vote number", "Title"]
        direction = request.form['direction'].lower()
        sort_by = request.form['sort_by'].lower()
        sorted_questions = utility.sort_question(sort_by, direction)
        return render_template("list.html", file=sorted_questions, fieldnames=fieldnames)


@app.route("/question/<id>", methods=['GET','POST'])
def question_route(id):
    if request.method == "GET":
        question = data_manager.get_question(id)
        answers = data_manager.get_all_answers(id)
        question_comments = data_manager.get_question_comments(id)
        return render_template("question-page.html", to_display=question, answers_to_display=answers, question_id=id, comments=question_comments)

@app.route("/add-question", methods=["GET", "POST"])
def add_question_route():
    if request.method == "POST":
        data_manager.add_question(request.form['title'], request.form['message'])
        return redirect("list")
    return render_template("add-question.html")


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def answer_route(question_id):
    if request.method == "GET":
        return render_template("add-answer.html", question_id=question_id)
    elif request.method == "POST":
        data_manager.add_answers(question_id, request.form['message'])
        return redirect(url_for("question_route", id=question_id))


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/question/<question_id>/edit", methods=["GET", "POST"])
def edit_route(question_id):
    if request.method == "GET":
        question = data_manager.get_question(question_id)
        return render_template("edit-question.html", question=question, question_id=question_id)
    elif request.method == "POST":
        title=request.form['title']
        message=request.form['message']
        data_manager.update_question("question",title,message,question_id)
        return redirect(url_for('question_route', id=question_id))

@app.route("/question/<question_id>/delete", methods=["GET","POST"])
def delete_question(question_id):
    answer_id=data_manager.get_answerId_by_questionId(question_id)
    data_manager.delete_row("comment", "answer_id", answer_id)
    data_manager.delete_row("comment", "question_id", question_id)
    data_manager.delete_row("answer", "question_id", question_id)
    data_manager.delete_row("question", "id", question_id)
    return redirect(url_for("list_route"))

@app.route("/answer/<answer_id>")
def see_answer_route(answer_id):
    answer=data_manager.get_answer(answer_id)
    answer_comments = data_manager.get_certain_answer_comments(answer_id)
    return render_template("answer-page.html", answer=answer, comments=answer_comments)


@app.route("/<question_id>/answer/<answer_id>/delete")
def delete_answer(answer_id, question_id):
    data_manager.delete_row("answer", "id", answer_id )
    return redirect(url_for('question_route' , id=question_id))

@app.route("/<question_id>/answer/<answer_id>/edit", methods=["GET", "POST"])
def edit_answer(answer_id, question_id):
    if request.method == "GET":
        answer = data_manager.get_answer(answer_id)
        return render_template("edit-answer.html", answer=answer, question_id=question_id)
    elif request.method == "POST":
        message=request.form['message']
        data_manager.update_answer(answer_id, message)
        return redirect(url_for('question_route', id=question_id))

@app.route('/answer/<answer_id>/new-comment', methods=['GET','POST'])
def add_comment_to_answer(answer_id):
    if request.method == 'GET':
        return render_template('add_coment_to_answer.html', answer_id=answer_id)
    elif request.method == "POST":
        data_manager.add_comment_ans(answer_id, request.form['comment_answer'])
        return redirect(url_for('see_answer_route', answer_id=answer_id))



@app.route("/question/<question_id>/new_comment", methods=["GET", "POST"])
def question_comment_route(question_id):
    if request.method == "GET":
        return render_template("add-question-comment.html", question_id=question_id)
    elif request.method == "POST":
        message=request.form['question-comment']
        question_id=question_id
        data_manager.add_question_comment(question_id,message)
        return redirect(url_for("question_route",id=question_id))

@app.route("/comments/<comment_id>/delete")
def delete_question_comments(comment_id):
    table = "comment"
    column = "id"
    question_id=data_manager.get_questionId_by_commentId(comment_id)
    data_manager.delete_row(table, column, comment_id)
    return redirect(url_for('question_route', id=question_id))

@app.route("/answer/<comment_id>/delete")
def delete_answer_comments(comment_id):
    table = "comment"
    column = "id"
    answer_id = data_manager.get_answerId_by_commentId(comment_id)
    data_manager.delete_row(table, column, comment_id)
    return redirect(url_for('see_answer_route', answer_id=answer_id))


@app.route("/comment/<comment_id>/edit", methods=["GET","POST"])
def edit_comment(comment_id):
    question_id = data_manager.get_questionId_by_commentId(comment_id)
    comment = data_manager.get_comment(question_id, comment_id)
    if request.method == "GET":
        return render_template("edit-comment.html", comment=comment)
    elif request.method == "POST":
        edited_comment = request.form['comment']
        data_manager.update_comment(edited_comment, comment_id)
        return redirect(url_for('question_route', id=question_id))

@app.route("/answer/<comment_id>/edit", methods=["GET","POST"])
def edit_answer_comment(comment_id):
    answer_id = data_manager.get_answerId_by_commentId(comment_id)
    comment = data_manager.get_answer_comment(comment_id)
    if request.method == "GET":
        return render_template('edit-answer-comment.html', comment=comment)
    elif request.method == "POST":
        edited_comment = request.form['comment']
        data_manager.answer_update_comment(edited_comment, comment_id)
        return redirect(url_for('see_answer_route', answer_id=answer_id))

@app.route("/question/<question_id>/vote_up")
def question_vote_up(question_id):
    data_manager.vote_question_up(question_id)
    return redirect(url_for('question_route', id=question_id))

@app.route("/question/<question_id>/vote_down")
def question_vote_down(question_id):
    data_manager.vote_question_down(question_id)
    return redirect(url_for('question_route', id=question_id))

@app.route("/answer/<answer_id>/vote_up")
def answer_vote_up(answer_id):
    data_manager.vote_answer_up(answer_id)
    question_id=data_manager.get_questionID_by_answerId(answer_id)
    return redirect(url_for("question_route",id=question_id))

@app.route("/answer/<answer_id>/vote_down")
def answer_vote_down(answer_id):
    data_manager.vote_answer_down(answer_id)
    question_id=data_manager.get_questionID_by_answerId(answer_id)
    return redirect(url_for("question_route",id=question_id))


@app.route("/search", methods=['GET','POST'])
def search_route():
    search_phrase=request.args.get('q')
    keyword_questions = data_manager.question_search_result(search_phrase)
    keyword_answers = data_manager.answer_search_result(search_phrase)
    return render_template("results-page.html", question_results=keyword_questions, answer_results=keyword_answers, phrase=search_phrase)

if __name__ == "__main__":
    app.run(debug=True,
            port=5000)
