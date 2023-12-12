from server import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

"""
werkzeug.security offers us a very good hashing algorithm.
we will use the generate_password_hash() function to generate 
a hash of the password before storing to database
"""


class User(UserMixin): # UserMixin gives us default implementations of is_authenticated() and is_active() functions

    def __init__(self, name, email, password, department):
        self.name = name
        self.email = email
        self.password = password
        self.department = department

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
        "department": user.department
    }) 

def get_user(email):
    """
    This function retrieves user data from database 
    by using their email
    """
    user = db.user_collection.find_one({'_id':email}) # This will return None if no data is returned
    if user is not None:
        return User(user['name'], user['_id'], user['password'], user['department'])
    
