from server import db


class User:

    def __init__(self, name, email, password, department):
        self.name = name
        self.email = email
        self.password = password
        self.department = department
        self.data = {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "department": self.department
        }

    # def save(self):
    #     try:
    #         with open("./data/users.json", mode="r") as file:
    #             existing_data = json.load(file)
    #             existing_data.update({self.email: self.data})  # Update with a dictionary
    #     except (FileNotFoundError, json.decoder.JSONDecodeError):
    #         existing_data = {self.email: self.data}  # If the file doesn't exist yet

    #     with open("./data/users.json", mode="w") as file:
    #         json.dump(existing_data, file, indent=4)

    def save(self):
        # Now if you open MongoDB you will find it listed here:
        db.user_collection.insert_one(self.data)


# # returns True if login information is valid
# def check_login(email, password):
#     try:
#         with open("./data/users.json", mode="r") as file:
#             data = json.load(file)
#             if email in data and password == data[email]["password"]:
#                 return True
#     except (FileNotFoundError, json.decoder.JSONDecodeError):
#         pass
#     return False

def check_login(email, password):
    # This will return a dict if we found the user with the email else None
    chk_user = db.user_collection.find_one({'email': email})
    if chk_user is not None:
        if chk_user['password'] == password:
            return True
    return False


# # returns True if user does not exist
# def check_new_user(email):
#     try:
#         with open("./data/users.json", mode="r") as file:
#             data = json.load(file)
#             if email in data:
#                 return False
#     except (FileNotFoundError, json.decoder.JSONDecodeError):
#         pass
#     return True


def check_new_user(email):
    # This will return a dict if we found the user with the email else None
    chk_user = db.user_collection.find_one({'email': email})
    if chk_user is not None:
        return False  # Meaning the email does exist, therefore user can't use the email
    return True 
