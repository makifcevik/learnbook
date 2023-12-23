from server import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

"""
werkzeug.security offers us a very good hashing algorithm.
we will use the generate_password_hash() function to generate 
a hash of the password before storing to database
"""


class User(UserMixin):  # UserMixin gives us default implementations of is_authenticated() and is_active() functions

    def __init__(self, name, email, password, department, user_follower_count=0, followed_id=[]):
        self.name = name
        self.email = email
        self.password = password
        self.department = department
        self.user_follower_count = user_follower_count
        self.followed_id = followed_id

    # # The following has to be written for LoginManager() to work
    def get_id(self):
        return self.email
    
    def is_anonymous(self):
        return False
    
    # def is_authenticated(self):
    #     return True
    
    # def is_active(self):
    #     return True
    
    def check_password(self, password_input):
        """
        This function is used during login to check the password input
        from the user to the hashed password stored in database
        """
        return check_password_hash(self.password, password_input)


def save_user(user):
    """
    This function is used during signup, it will hash the password
    then store user's email, name, password, and department in database

    You may check the MongoDB database for results
    """
    password_hash = generate_password_hash(user.password)
    db.user_collection.insert_one({
        "_id": user.email,
        "name": user.name,
        "password": password_hash,
        "department": user.department,
        "user_follower_count": user.user_follower_count,
        "followed_id": user.followed_id
    }) 


def get_user(email):
    """
    This function retrieves user data from database 
    by using their email
    """
    user = db.user_collection.find_one({'_id': email})  # This will return None if no data is returned
    if user is not None:
        return User(user['name'], user['_id'], user['password'], user['department'], user['user_follower_count'], user['followed_id'])
    else:
        return None


def get_username(email):
    user = db.user_collection.find_one({'_id': email}, {'name': 1, '_id': 0})

    if user is not None and 'name' in user:
        return user['name']
    else:
        return None
    
