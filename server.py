from flask import Flask , request, redirect, render_template, url_for

app = Flask(__name__, template_folder="template", static_folder="static")

@app.route("/")
def index_route():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(
        Debug=True,
        Port=5000
    )