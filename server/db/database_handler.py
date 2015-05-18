import sqlite3

class Database_Connection():
    def __init__(self, db_name):
        self.db = sqlite3.connect(db_name)
        
    def user_in_db(self, username):
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM user WHERE name="?"', username)
        print(cursor)
        return False

    def authenticate_user(self, username, password):
        return False

    def create_user(self, username, password):
        return False

    def print_database(self):
        print("Please implement me")

# For Testing
if (__name__ == "__main__"):
    db = Database_Connection("users_test.db")
    print(db.user_in_db("test"))
"""
user(name TEXT, password TEXT, win INT, game INT, PRIMARY KEY(name))
"""

"""
t = ('IBM',)
c.execute('select * from stocks where symbol=?', t)

# Larger example
for t in [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
          ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
          ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
         ]:
    c.execute('insert into stocks values (?,?,?,?,?)', t)
"""
