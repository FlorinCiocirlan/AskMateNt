from flask import Flask , request, redirect, render_template, url_for
import connection, data_manager, utility

app = Flask(__name__, template_folder="template", static_folder="static")

@app.route("/")
def index_route():
    return render_template("index.html")

@app.route("/list")
def list_route():
    dicti = connection.read_from_csv("sample_data/question.csv")
    return render_template("list.html", file = dicti)

if __name__ == "__main__":
    app.run(debug=True,
            port=5000)