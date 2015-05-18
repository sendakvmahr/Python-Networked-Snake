import sqlite3

class Database_Connection():
    def __init__(self, db_name):
        self.db = sqlite3.connect(db_name)

    def user_in_db(self, username):
        return False

    def authenticate_user(self, username, password):
        return False

    def create_user(self, username, password):
        return False

    def print_database(self):
        print("Please implement me")


# For Testing
if (__name__ == "__main__"):
    c = Database_Connection("users_test.db")
    
