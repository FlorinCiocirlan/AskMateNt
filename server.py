from flask import Flask, request, redirect, render_template, url_for, session, flash
import connection, data_manager, utility
import os, sys

UPLOAD_FOLDER = 'static/images'

app = Flask(__name__, template_folder="template", static_folder="static")
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
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
        answer_user_data=data_manager.find_username_for_answer(id)

        question_user_data=data_manager.find_username_by_question_id(id)
        quest_comm_user_data = data_manager.find_userdata_for_questions_comments(id)
        question = data_manager.get_question(id)
        answers = data_manager.get_all_answers(id)
        question_comments = data_manager.get_question_comments(id)
        return render_template("question-page.html", to_display=question,q_user_data=question_user_data,
                               a_user_data=answer_user_data, answers_to_display=answers, question_id=id,
                               comments=question_comments, quest_comm_user_data=quest_comm_user_data)

@app.route("/add-question", methods=["GET", "POST"])
def add_question_route():
    if session.get('username') is not None:
        if request.method == "POST":
            data_manager.add_question(request.form['title'], request.form['message'],session['user_id'])
            return redirect("list")
        return render_template("add-question.html")
    else:
        flash('You must login before using features','no_user')
        return redirect(url_for('index_route'))


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def answer_route(question_id):
    if session.get('username') is not None:
        if request.method == "GET":
            return render_template("add-answer.html", question_id=question_id)
        elif request.method == "POST":
            message=request.form['message']
            user_id=session['user_id']
            data_manager.add_answers(question_id, message,user_id)
            return redirect(url_for("question_route", id=question_id))
    else:
        flash('You must login before using features', 'no_user')
        return redirect(url_for('question_route',id=question_id))


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/question/<question_id>/edit", methods=["GET", "POST"])
def edit_route(question_id):
    if session.get('username') is not None:
        question_user_id=data_manager.find_userid_by_questionid(question_id)
        if question_user_id:
            if session['user_id'] == question_user_id['user_id'] or session['username'] == 'administrator':
                if request.method == "GET":
                    question = data_manager.get_question(question_id)
                    return render_template("edit-question.html", question=question, question_id=question_id)
                elif request.method == "POST":
                    title=request.form['title']
                    message=request.form['message']
                    data_manager.update_question("question",title,message,question_id)
                    return redirect(url_for('question_route', id=question_id))
            else:
                flash("You dont have acces","no_acces")
                return redirect(url_for('question_route', id=question_id))
    else:
        flash('You must login before using features', 'no_user')
        return redirect(url_for('question_route', id=question_id))

@app.route("/question/<question_id>/delete", methods=["GET","POST"])
def delete_question(question_id):
    if session.get('username') is not None:
        question_user_id=data_manager.find_userid_by_questionid(question_id)
        if question_user_id:
            if session['user_id'] == question_user_id['user_id'] or session['username'] == 'administrator':
                data_manager.delete_row("question", "id", question_id)
                return redirect(url_for("list_route"))
            else:
                flash("You dont have acces", "no_acces")
                return redirect(url_for('question_route', id=question_id))
    else:
        flash('You must login before using features', 'no_user')
        return redirect(url_for('question_route', id=question_id))

@app.route("/answer/<answer_id>")
def see_answer_route(answer_id):
    answer=data_manager.get_answer(answer_id)
    answer_comments = data_manager.get_certain_answer_comments(answer_id)
    ans_comm_user_data = data_manager.find_userdata_for_answers_comments(answer_id)
    return render_template("answer-page.html", answer=answer, comments=answer_comments,
                           ans_comm_user_data=ans_comm_user_data)


@app.route("/<question_id>/answer/<answer_id>/delete")
def delete_answer(answer_id, question_id):
    if session.get('username') is not None:
        answer_user_id=data_manager.find_userid_by_answerid(answer_id)
        if answer_user_id:
            if session['user_id'] == answer_user_id['user_id'] or session['username'] == 'administrator':
                data_manager.delete_row("answer", "id", answer_id)
                return redirect(url_for('question_route' , id=question_id))
            else:
                flash("You dont have acces", "no_acces")
                return redirect(url_for('question_route', id=question_id))
    else:
        flash('You must login before using features', 'no_user')
        return redirect(url_for('question_route', id=question_id))

@app.route("/<question_id>/answer/<answer_id>/edit", methods=["GET", "POST"])
def edit_answer(answer_id, question_id):
    if session.get('username') is not None:
        answer_user_id = data_manager.find_userid_by_answerid(answer_id)
        if answer_user_id:
            if session['user_id'] == answer_user_id['user_id'] or session['username'] == 'administrator':
                if request.method == "GET":
                    answer = data_manager.get_answer(answer_id)
                    return render_template("edit-answer.html", answer=answer, question_id=question_id)
                elif request.method == "POST":
                    message=request.form['message']
                    data_manager.update_answer(answer_id, message)
                    return redirect(url_for('question_route', id=question_id))
            else:
                flash("You dont have acces", "no_acces")
                return redirect(url_for('question_route', id=question_id))

    else:
        flash('You must login before using features', 'no_user')
        return redirect(url_for('question_route', id=question_id))

@app.route('/answer/<answer_id>/new-comment', methods=['GET','POST'])
def add_comment_to_answer(answer_id):
    if session.get('username') is not None:
        if request.method == 'GET':
            return render_template('add_coment_to_answer.html', answer_id=answer_id)
        elif request.method == "POST":
            user_id = session['user_id']
            comment=request.form['comment_answer']
            data_manager.add_comment_ans(answer_id, comment, user_id)
            return redirect(url_for('see_answer_route', answer_id=answer_id))
    else:
        flash('You must login before using features', 'no_user')
        return redirect(url_for('see_answer_route', answer_id=answer_id))



@app.route("/question/<question_id>/new_comment", methods=["GET", "POST"])
def question_comment_route(question_id):
    if session.get('username') is not None:
        if request.method == "GET":
            return render_template("add-question-comment.html", question_id=question_id)
        elif request.method == "POST":
            message=request.form['question-comment']
            question_id=question_id
            user_id = session['user_id']
            data_manager.add_question_comment(question_id,message,user_id)
            return redirect(url_for("question_route",id=question_id))
    else:
        flash('You must login before using features', 'no_user')
        return redirect(url_for('question_route', id=question_id))

@app.route("/comments/<comment_id>/delete")
def delete_question_comments(comment_id):
    question_id = data_manager.get_questionId_by_commentId(comment_id)
    if session.get('username') is not None:
        comment_user_id=data_manager.find_userid_by_commentid(comment_id)
        if comment_user_id:
            if session['user_id'] == comment_user_id['user_id'] or session['username'] == 'administrator':
                table = "comment"
                column = "id"
                data_manager.delete_row(table, column, comment_id)
                return redirect(url_for('question_route', id=question_id))
            else:
                flash("You dont have acces", "no_acces")
                return redirect(url_for('question_route', id=question_id))
    else:
        flash('You must login before using features', 'no_user')
        return redirect(url_for('question_route', id=question_id))

@app.route("/answer/<comment_id>/delete")
def delete_answer_comments(comment_id):
    answer_id = data_manager.get_answerId_by_commentId(comment_id)
    if session.get('username') is not None:
        answer_comment_id=data_manager.find_userid_by_commentid(comment_id)
        if answer_comment_id:
            if session['user_id'] == answer_comment_id['user_id'] or session['username'] == 'administrator':
                table = "comment"
                column = "id"
                data_manager.delete_row(table, column, comment_id)
                return redirect(url_for('see_answer_route', answer_id=answer_id))
            else:
                flash("You dont have acces", "no_acces")
                return redirect(url_for('see_answer_route', answer_id=answer_id))
    else:
        flash('You must login before using features', 'no_user')
        return redirect(url_for('see_answer_route', answer_id=answer_id))


@app.route("/comment/<comment_id>/edit", methods=["GET","POST"])
def edit_comment(comment_id):
    question_id=data_manager.get_questionId_by_commentId(comment_id)
    if session.get('username') is not None:
        comment_user_id=data_manager.find_userid_by_commentid(comment_id)
        if comment_user_id:
            if session['user_id'] == comment_user_id['user_id'] or session['username'] == 'administrator':
                comment = data_manager.get_comment(question_id, comment_id)
                if request.method == "GET":
                    return render_template("edit-comment.html", comment=comment)
                elif request.method == "POST":
                    edited_comment = request.form['comment']
                    data_manager.update_edited_count(comment_id)
                    data_manager.update_comment(edited_comment, comment_id)
                    return redirect(url_for('question_route', id=question_id))
            else:
                flash("You dont have access", "no_acces")
                return redirect(url_for('question_route', id=question_id))
    else:
        flash('You must login before using features', 'no_user')
        return redirect(url_for('question_route', id=question_id))



@app.route("/answer/<comment_id>/edit", methods=["GET","POST"])
def edit_answer_comment(comment_id):
    answer_id=data_manager.get_answerId_by_commentId(comment_id)
    if session.get('username') is not None:
        comment_user_id=data_manager.find_userid_by_commentid(comment_id)
        if comment_user_id:
            if session['user_id'] == comment_user_id['user_id'] or session['username'] == 'administrator':
                comment = data_manager.get_answer_comment(comment_id)
                if request.method == "GET":
                    return render_template('edit-answer-comment.html', comment=comment)
                elif request.method == "POST":
                    edited_comment = request.form['comment']
                    data_manager.update_edited_count(comment_id)
                    data_manager.update_comment(edited_comment, comment_id)
                    return redirect(url_for('see_answer_route', answer_id=answer_id))
            else:
                flash("You dont have access", "no_acces")
                return redirect(url_for('see_answer_route', answer_id=answer_id))
    else:
        flash('You must login before using features', 'no_user')
        return redirect(url_for('see_answer_route', answer_id=answer_id))

@app.route("/question/<question_id>/vote_up")
def question_vote_up(question_id):
    if session.get['username'] is not None:
        data_manager.vote_question_up(question_id)
        return redirect(url_for('question_route', id=question_id))

@app.route("/question/<question_id>/vote_down")
def question_vote_down(question_id):
    if session.get['username'] is not None:
        data_manager.vote_question_down(question_id)
        return redirect(url_for('question_route', id=question_id))

@app.route("/answer/<answer_id>/vote_up")
def answer_vote_up(answer_id):
    if session.get['username'] is not None:
        data_manager.vote_answer_up(answer_id)
        question_id=data_manager.get_questionID_by_answerId(answer_id)
        return redirect(url_for("question_route",id=question_id))

@app.route("/answer/<answer_id>/vote_down")
def answer_vote_down(answer_id):
    if session.get['username'] is not None:
        data_manager.vote_answer_down(answer_id)
        question_id=data_manager.get_questionID_by_answerId(answer_id)
        return redirect(url_for("question_route",id=question_id))


@app.route("/search", methods=['GET','POST'])
def search_route():
    search_phrase=request.args.get('q')
    keyword_questions = data_manager.question_search_result(search_phrase)
    keyword_answers = data_manager.answer_search_result(search_phrase)
    return render_template("results-page.html", question_results=keyword_questions, answer_results=keyword_answers, phrase=search_phrase)

@app.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = utility.hash_password(request.form['password'])
        if data_manager.if_already_exist('email',email) or data_manager.if_already_exist('username',username):
            flash('Username or Email Adress already in use')
            return render_template('register.html')
        else:
            data_manager.insert_user(username, password, email)
            return redirect(url_for('login'))
    return render_template("register.html")

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if data_manager.if_already_exist('username', username):
            hashed_password = data_manager.get_hashed_password(username)
            if utility.verify_password(password,hashed_password):
                session['username'] = username
                session['user_id'] = data_manager.find_id_by_username(username)
                flash(f"You are logged in as {username}", "succesful_login")
                return redirect(url_for('index_route'))
            else:
                flash("Invalid username or password","invalid_login")
        else:
            flash("Invalid username or password","invalid_login")
    return render_template('login.html')

@app.route("/logout")
def logout():
    session.pop('username')
    session.pop('user_id')
    return redirect(url_for('index_route'))

@app.route("/user")
def user():
    fieldname = ["Question title", "Question message", "Answer message", "Comment message"]
    user = data_manager.get_user_data(session['user_id'])
    return render_template('user.html', user=user, fieldname=fieldname)



if __name__ == "__main__":
    app.run(debug=True,
            port=5000)
