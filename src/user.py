import json


class User:

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.data = {
            "name": self.name,
            "email": self.email,
            "password": self.password,
        }

    def save(self):
        try:
            with open("../data/users.json", mode="r") as file:
                existing_data = json.load(file)
                existing_data.update({self.email: self.data})  # Update with a dictionary
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            existing_data = {self.email: self.data}  # If the file doesn't exist yet

        with open("../data/users.json", mode="w") as file:
            json.dump(existing_data, file, indent=4)


# returns True if login information is valid
def check_login(email, password):
    try:
        with open("../data/users.json", mode="r") as file:
            data = json.load(file)
            if email in data and password == data[email]["password"]:
                return True
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        pass
    return False


# returns True if user does not exist
def check_new_user(email):
    try:
        with open("../data/users.json", mode="r") as file:
            data = json.load(file)
            if email in data:
                return False
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        pass
    return True
