from flask import Flask, render_template, redirect, url_for, request, session
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_socketio import SocketIO, join_room, leave_room
import re
from user import *

# Flask app setup
app = Flask(__name__)
app.config['SECRET_KEY'] = '72de10f502ec243d7ab803524a1f0385'
socketio = SocketIO(app, cors_allowed_origins="*")

# MongoDB database setup
app.config['MONGO_URI'] = "mongodb://localhost:27017/user"  # Location of MongoDB database
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
        _user = _user.lower()
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


@app.route("/")
@login_required
def user():
    """
    This function returns the user homepage IF they
    are logged in otherwise return them the login page
    """
    if "user" in session:
        _user = session["user"]
        return render_template("home_page.html", current_user=current_user)
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
    This function returns the sign-up page,
    It asks for name, email, password, and department.

    After submitting, it will check if the email already exist in database,
    also check if the user is using the correct email extension ('bilgiedu.net')
    If it does exist then redirect them to the same page with an error message
    otherwise save information to database and redirect them to homepage
    """

    pattern = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@bilgiedu.net')
    message = ''
    if request.method == "POST":
        _name = request.form["name"]
        _email = request.form["email"]
        _password = request.form["password"]
        _department = request.form["department"]
        
        _email = _email.lower()
        # checking if the user already exists
        if re.fullmatch(pattern, _email):
            try:
                new_user = User(_name, _email, _password, _department)
                save_user(new_user)
                login_user(new_user)
                session["user"] = _email
                return redirect(url_for("user"))
            except DuplicateKeyError:
                message = 'User already exist, please try another email'
        else:
            message = 'Please ensure you use an email with a "@bilgiedu.net" extension'

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

    # Check if the current user already followed the other user
    if db.user_collection.find_one({'followed_id': email}, {'followed_id': 1}):
        is_followed = 'Unfollow'
    else:
        is_followed = 'Follow'

    return render_template('user-profile-other.html', user=usr, is_followed=is_followed)


@app.route('/community/')
@login_required
def community_profile_page():
    """
    This function returns the communities profile pages;
    A login is required to access this page.
    """
    name = request.args.get('name')
    community = db.community_collection.find_one({'name': name})

    # Check if the current user already followed this community
    if db.user_collection.find_one({'followed_community': name}, {'followed_community':1}):
        is_joined = 'Unfollow'
    else:
        is_joined = 'Join'

    return render_template('community-profile.html', community=community, is_joined=is_joined)


@app.route('/chat')
@login_required
def chat():
    """
    This function returns the chat page;
    A login is required to access this page
    """
    return render_template('chat_page.html', current_user=current_user)


@app.route('/profile_page')
@login_required
def profile_page():
    """
    This function returns the current user's profile page;
    A login is required to access this page
    """

    user = get_user(current_user.email)
    return render_template('user-profile-user.html', user=user)


@socketio.on('start_chat')
def handle_start_chat(data):
    current_username = get_username(session["user"])
    target_username = data['target_username']

    # Create a sorted list of usernames to ensure consistency in the chat room name
    user_list = sorted([current_username, target_username])

    # Create a unique chat room identifier based on the sorted list of usernames
    room = f'chat_{user_list[0]}_{user_list[1]}'

    # Join the chat room
    join_room(room)

    # Emit a welcome message to both users in the chat
    # socketio.emit('chat_message', {'message': f'Welcome to the chat, {current_username} and {target_username}!'},
    #               room=room)


@socketio.on('send_message')
def handle_send_message(data):
    current_username = get_username(session["user"])
    target_username = data['target_username']
    message = data['message']

    # Create a sorted list of usernames to ensure consistency in the chat room name
    user_list = sorted([current_username, target_username])

    # Create a unique chat room identifier based on the sorted list of usernames
    room = f'chat_{user_list[0]}_{user_list[1]}'

    # Broadcast the message to everyone in the chat room
    socketio.emit('chat_message', {'username': current_username, 'message': message}, room=room)


@socketio.on('leave_chat')
def handle_leave_chat(data):
    current_username = get_username(session["user"])
    target_username = data['target_username']

    # Create a sorted list of usernames to ensure consistency in the chat room name
    user_list = sorted([current_username, target_username])

    # Create a unique chat room identifier based on the sorted list of usernames
    room = f'chat_{user_list[0]}_{user_list[1]}'

    # Leave the chat room
    leave_room(room)
    # print(f'{current_username} left the chat with {target_username}')


# @socketio.on("message_sent")
# def handle_message_sent(message_sent):
#     _user = get_user(session["user"])
#     if _user is not None:
#         _name = _user.name
#         message = message_sent
#         data = {'user': f'{_name}', 'message': message}
#         socketio.emit("message", data)


@socketio.on('searchFunction')
def search_function(search_query):
    """
    After receiving an input on the search bar from the current user,
    this function will look through the database using such input and then it 
    will return a series of documents(result) to the current user's browser.

    This function will fire up the 'printSearchResult' event on the browser
    located at 'search.html'.

    Note: Community Id is not returned because it caused some errors, '_id':False for now
    """
    results_community = list(db.community_collection.find({"name": {'$regex': '^' + search_query, '$options': 'i'}},
                                                          {'_id': False}))

    results_people = list(db.user_collection.find({'$and': [{"name": {'$regex': '^' + search_query, '$options': 'i'}},
                                                            {'_id': {'$ne': current_user.email}}]}))

    socketio.emit('printSearchResult', [results_people, results_community])


@socketio.on('follow_user')
def follow_user(followed_id):
    """
    This function is called after the current user requests to follow another user.
    This is done by pushing the user's (to be followed) email to the current user's list
    of 'followed' in database and then increment the followed count of the current user by 1
    """

    db.user_collection.update_one({"_id": current_user.email},
                                  {"$push": {"followed_id": followed_id},
                                   "$inc": {"user_follower_count": 1}})
    socketio.emit('adjustFollowedPage')


@socketio.on('unfollow_user')
def unfollow_user(followed_id):
    """
    This function is called after the current user requests to unfollow another user.
    This is done by pulling (removing) the user's (to be unfollowed) email from the current user's list
    of 'followed' in database and then decrementing the followed count of the current user by 1
    """
    db.user_collection.update_one({"_id": current_user.email},
                                  {"$pull": {"followed_id": followed_id},
                                   "$inc": {"user_follower_count": -1}})
    socketio.emit('adjustUnfollowedPage')

@socketio.on('joinClub')
def joinClub(club_name):
    """
    This function is called after the current user requests to join a club.
    This is done by pushing (adding) the club's name to the current user's list of joined clubs
    in database and then incrementing the followed community counter by 1
    """

    db.user_collection.update_one({"_id": current_user.email},
                                  {"$push": {"followed_community": club_name},
                                   "$inc": {"user_community_count": 1}})
    
    db.community_collection.update_one({"name": club_name}, {"$inc": {"followers": 1}})
    socketio.emit('adjustJoinedPage')

@socketio.on('unfollowClub')
def unfollowClub(club_name):
    """
    This function is called after the current user requests to unfollow a club.
    This is done by pulling (removing) the club's name from the current user's list of joined clubs
    in database and then decrementing the followed community counter by 1
    """
    db.user_collection.update_one({"_id": current_user.email},
                                  {"$pull": {"followed_community": club_name},
                                   "$inc": {"user_community_count": -1}})
    
    db.community_collection.update_one({"name": club_name}, {"$inc": {"followers": -1}})
    socketio.emit('adjustUnfollowedPage')

    


# Start app
if __name__ == "__main__":
    # app.run(debug=True)
    # Put your own ipv4 address or put "localhost"
    # If you want to use the chat put the same thing on chat.js file too. Unless you want
    # to use the chat it is not necessary
    socketio.run(app, host="localhost", allow_unsafe_werkzeug=True, debug=True)
