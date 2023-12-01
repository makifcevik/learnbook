from flask import Flask, render_template, redirect, url_for, request, session, flash
from user import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'DF48JD459'

# for test only (already exists in ./data/users.json)
# user_admin = User(name="Admin", email="admin@", password="1234")
# user_admin.save()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    # login user
    if request.method == "POST":
        _user = request.form["email"]
        _password = request.form["password"]

        # check information
        if check_login(_user, _password):
            session["user"] = _user
            return redirect(url_for("user"))
        # if the information is invalid redirect to the same page (temporary, later there'll be an alert message)
        else:
            return redirect(url_for("login"))
    else:
        # already logged in user
        if "user" in session:
            return redirect(url_for("user"))

        # not logged in user
        return render_template("login.html")


@app.route("/user")
def user():
    # generate the page for the user if exists
    if "user" in session:
        _user = session["user"]
        return f"<h1>{_user}</h1>"
    # user does not exist
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/sign-up", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        _name = request.form["name"]
        _email = request.form["email"]
        _password = request.form["password"]

        # checking if the user already exists
        if check_new_user(_email):
            new_user = User(_name, _email, _password)
            new_user.save()
            print(new_user)
            session["user"] = _name
            return redirect(url_for("user"))
        # if it already exists redirect to the same page (temporary, later there'll be an alert message)
        else:
            return redirect(url_for("sign_up"))
    else:
        return render_template("sign-up.html")


if __name__ == "__main__":
    app.run(debug=True)
