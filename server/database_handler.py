import sqlite3

class Database_Connection():
    def __init__(self, db_name):
        self.db = sqlite3.connect(db_name)
        
    def user_in_db(self, username):
        results = self._execute_command('SELECT * FROM user WHERE name=?', (username,))
        return len(results) != 0

    def authenticate_user(self, username, password):
        results = self._execute_command('SELECT name, password FROM user WHERE name=? AND password=?', (username, password))
        return len(results) != 0

    def create_user(self, username, password):
        try:
            self._execute_command("insert into user(name, password, win, game) values (?, ?, ?, ?)", (username, password, 0, 0))
            self.db.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def print_database(self):
        results = self._execute_command('SELECT * FROM user', tuple())
        for r in results:
            print("Name: {}\t Pw: {}\t Win: {}\t Games: {}\t".format(r[0], r[1], r[2], r[3]))

    def _execute_command(self, command, args):
        cursor = self.db.cursor()
        cursor.execute(command, args)
        result = [r for r in cursor]
        cursor.close()
        return result

    def __exit__(self):
        self.db.commit()
        self.db.close()
    

# For Testing
if (__name__ == "__main__"):
    """
    db = Database_Connection(":memory:")
    # Also schema for db
    db.db.execute("create table user(name TEXT, password TEXT, win INT, game INT, PRIMARY KEY(name))")
    db.create_user("test", "test")
    db.create_user("ouroboros", "tiamat")
    assert(db.user_in_db("test"))
    assert(not db.user_in_db("wertizoo"))
    assert(db.authenticate_user("test", "test"))
    assert(not db.authenticate_user("test", "wrong"))
    db.print_database()
    """
    db = Database_Connection("users.db")
    #db.create_user("test2", "test")
    
    db.print_database()
