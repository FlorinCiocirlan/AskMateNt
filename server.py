from flask import Flask, request, redirect, render_template, url_for,flash
import connection, data_manager, utility
import os, sys
from werkzeug.utils import secure_filename
from forms import RegistrationForm,LoginForm

app = Flask(__name__, template_folder="template", static_folder="static", )
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

UPLOAD_FOLDER = 'static/images'

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


@app.route("/question/<id>")
def question_route(id):
    question = data_manager.get_question(id)
    answers = data_manager.get_all_answers(id)
    comments = data_manager.get_question_comments(id)
    return render_template("question-page.html", to_display=question, answers_to_display=answers, question_id=id, comments=comments)


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
    data_manager.delete_row("answer", "question_id", question_id)
    data_manager.delete_row("question", "id", question_id)
    return redirect(url_for("list_route"))

@app.route("/<question_id>/answer/<answer_id>/delete")
def delete_answer(answer_id, question_id):
    data_manager.delete_row("answer", "id", answer_id )
    return redirect(url_for('question_route' , id=question_id))

@app.route("/<question_id>/answer/<answer_id>/edit", methods=["GET", "POST"])
def edit_answer(answer_id, question_id):
    if request.method == "GET":
        answer = utility.get_answer(answer_id,question_id)
        return render_template("edit-answer.html", answer=answer, question_id=question_id)
    elif request.method == "POST":
        message=request.form['message']
        data_manager.update_answer(answer_id, message)
        return redirect(url_for('question_route', id=question_id))

@app.route('/answer/<answer_id>/new-comment', methods=['GET','POST'])
def add_comment_to_answer(answer_id):
    if request.method == 'GET':
        return render_template('add_coment_to_answer.html', answer_id=answer_id)
    if request.method == "POST":
        data_manager.add_comment_ans(answer_id, request.form['comment_answer'])
        return redirect(url_for('question_route', id=answer_route))
    return render_template('question-page.html')



@app.route("/question/<question_id>/new_comment", methods=["GET", "POST"])
def question_comment_route(question_id):
    if request.method == "GET":
        return render_template("add-question-comment.html", question_id=question_id)

@app.route("/question/<question_id>/vote", methods=["GET","POST"])
def vote_route(question_id):
    if request.method == "POST":
        new_vote=request.form['vote']
        utility.vote_question(question_id, new_vote)
        return redirect(url_for('question_route', id=question_id))

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index_route'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('index_route'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == "__main__":
    app.run(debug=True,
            port=5000)
