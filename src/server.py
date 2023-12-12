from flask import Flask, render_template, redirect, url_for, request, session
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from user import *

# Flask app setup
app = Flask(__name__)
app.config['SECRET_KEY'] = '72de10f502ec243d7ab803524a1f0385'

# MongoDB database setup
app.config['MONGO_URI'] = 'mongodb://localhost:27017/user' # Location of MongoDB database
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
def request_loader(request):
    email = request.form.get('email')
    return get_user(email)


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login", methods=["POST", "GET"])
def login():
    """
    This function returns the login page
    It asks for the email and password, and after submitting 
    it locates the user in database and compares the credentials.
    if authorized it will refer the user to the homepage otherwise
    it would display a login error
    """

    message = '' # Error message
    if request.method == "POST":
        _user = request.form["email"]
        _password = request.form["password"]

        user = get_user(_user) # User()
        # check information
        if user and user.check_password(_password): 
            # if the information is valid redirect to the homepage
            login_user(user)
            session["user"] = _user
            return redirect(url_for("user"))
        else:
            # if the information is invalid redirect to the same page and display error
            message = 'Failed to login'
            return render_template('login.html', message=message)
        
    else: # For the case of a "GET" request
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
        return f'''
            <h1>{_user}</h1>
            <a href="{url_for("logout")}">Logout</a>
        '''
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

    if current_user.is_authenticated():
        return redirect(url_for('user'))

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
    

@app.route('/search', methods=['POST', 'GET'])
@login_required
def search():
    """
    This function returns the search page.
    users can search for other users or communities to follow
    """
    results=''
    if request.method == 'POST':
        search_query =  request.form.get('search')
        choice = request.form.get('user_or_community')

        # find() method will return a Cursor instance which then we turn to a list
        # We use regex to filter the search (^: starts with; "$options:i": makes search insensitive to capital letters)
        if choice == 'community':
            results = list(db.community_collection.find({"name":{'$regex': '^'+search_query, '$options':'i'}}))
            return render_template('search.html', results=results)
        elif choice == 'user':
            results = list(db.user_collection.find({"name":{'$regex': '^'+search_query, '$options':'i'}}))
            return render_template('search.html', results=results)
        
    return render_template('search.html', results = results)

@app.route('/chat')
@login_required
def chat():
    """
    This function returns the chat page; A login
    is required to access this page
    """
    return render_template('chat_page.html')

@app.route('/profile_page')
@login_required
def profile_page():
    return render_template('current_user_profile.html', current_user=current_user)

# Start app
if __name__ == "__main__":
    app.run(debug=True)
