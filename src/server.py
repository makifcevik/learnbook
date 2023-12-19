from flask import Flask, render_template, redirect, url_for, request, session
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_socketio import SocketIO, send
from user import *

# Flask app setup
app = Flask(__name__)
app.config['SECRET_KEY'] = '72de10f502ec243d7ab803524a1f0385'
socketio = SocketIO(app, cors_allowed_origins="*")

# MongoDB database setup
app.config['MONGO_URI'] = "mongodb://localhost:27017/user" # Location of MongoDB database
mongodb_client = PyMongo(app)
db = mongodb_client.db

# Flask LoginManager setup
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(email):
    return get_user(email)


@login_manager.request_loader
def request_loader(req):
    email = req.form.get('email')
    return get_user(email)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    """
    This function returns the login page
    It asks for the email and password, and after submitting 
    it locates the user in database and compares the credentials.
    if authorized it will refer the user to the homepage otherwise
    it would display a login error
    """

    message = ''  # Error message
    if request.method == "POST":
        _user = request.form["email"]
        _password = request.form["password"]

        usr = get_user(_user)
        # check information
        if usr and usr.check_password(_password):
            # if the information is valid redirect to the homepage
            login_user(usr)
            session["user"] = _user
            return redirect(url_for("user"))
        else:
            # if the information is invalid redirect to the same page and display error
            message = 'Failed to login'
            return render_template('login.html', message=message)
        
    else:  # For the case of a "GET" request
        # already logged in user
        if "user" in session:
            return redirect(url_for("user"))
        else:
            return render_template("login.html", message=message)


@app.route("/user")
def user():
    """
    This function returns the user homepage IF they
    are logged in otherwise return them the login page
    """
    if "user" in session:
        _user = session["user"]
        return render_template("chat_page.html")
    # user does not exist
    else:
        return redirect(url_for("login"))


@app.route("/logout/")
@login_required
def logout():
    """
    This function logs out the user and takes them back to the 
    login page
    """
    logout_user()
    session.pop('user', None)
    return redirect(url_for("login"))


@app.route("/sign-up", methods=["POST", "GET"])
def sign_up():
    """
    This function returns the sign up page,
    It asks for name, email, password, and department.

    After submitting it will check if the email already exist in database,
    If it does exist then redirect them to the same page with an error message
    otherwise save information to database and redirect them to homepage
    """

    message = ''
    if request.method == "POST":
        _name = request.form["name"]
        _email = request.form["email"]
        _password = request.form["password"]
        _department = request.form["department"]

        # checking if the user already exists
        try:
            new_user = User(_name, _email, _password, _department)
            save_user(new_user)
            login_user(new_user)
            session["user"] = _email
            return redirect(url_for("user"))
        except DuplicateKeyError:
            message = 'User already exist, please try another email'
        # if it already exists redirect to the same page (temporary, later there'll be an alert message)
    
    return render_template("sign-up.html", message=message)


@app.route('/search')
@login_required
def search():
    """
    This function returns the search page allowing the users to find
    other users, or communities to follow;
    A login is required to access this page.
    """
    return render_template('search.html')


@app.route('/users/')
@login_required
def user_profile_page():
    """
    This function returns the profile page of users other than the current user;
    A login is required to access this page.
    """
    email = request.args.get('email')
    usr = get_user(email)
    return render_template('user_profile.html', user=usr)


@app.route('/community/')
@login_required
def community_profile_page():
    """
    This function returns the communities profile pages;
    A login is required to access this page.
    """
    name = request.args.get('name')
    community = db.community_collection.find_one({'name':name})
    return render_template('community-profile.html', community=community)


@app.route('/chat')
@login_required
def chat():
    """
    This function returns the chat page;
    A login is required to access this page
    """
    return render_template('chat_page.html')


@app.route('/profile_page')
@login_required
def profile_page():
    """
    This function returns the current user's profile page;
    A login is required to access this page
    """
    return render_template('current_user_profile.html', current_user=current_user)


@socketio.on("message")
def handle_message(message):
    _user = get_user(session["user"])
    if _user is not None:
        _name = _user.name
        message = f"{_name}: {message}"
        socketio.emit("message", message)


@socketio.on('searchFunction')
def search_function(search_query):
    """
    After receiving an input on the search bar from the current user,
    this function will look through the database using such input and then it 
    will return a series of documents(result) to the current user's browser.

    This function will fire up the 'printSearchResult' event on the browser
    located at 'search.html'.

    Note: Community Id is not returned because it caused some errors, '_id':False for now
    TODO: Make the search so it doesnt return the current user as the result
    """
    results_community = list(db.community_collection.find({"name":{'$regex': '^'+search_query, '$options':'i'}}, {'_id':False}))
    results_people = list(db.user_collection.find({"name":{'$regex': '^'+search_query, '$options':'i'}}))

    socketio.emit('printSearchResult', [results_people, results_community])


# Start app
if __name__ == "__main__":
    # app.run(debug=True)
    # Put your own ipv4 address or put "localhost"
    # If you want to use the chat put the same thing on chat.js file too. Unless you want
    # to use the chat it is not necessary
    # 105
    socketio.run(app, host="localhost", allow_unsafe_werkzeug=True, debug=True)
    # socketio.run(app, debug=True)

