from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/sign-up")
def sing_up():
    return render_template("sign-up.html")


if __name__ == "__main__":
    app.run(debug=True)
