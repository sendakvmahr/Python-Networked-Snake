import sqlite3
import hashlib

class Database_Connection():
    def __init__(self, db_name):
        self.db = sqlite3.connect(db_name)
        
    def user_in_db(self, username):
        results = self._execute_command('SELECT * FROM user WHERE name=?', (username,))
        return len(results) != 0

    def authenticate_user(self, username, password):
        password = self._hash(password)
        results = self._execute_command('SELECT name, password FROM user WHERE name=? AND password=?', (username, password))
        return len(results) != 0

    def create_user(self, username, password):
        password = self._hash(password)
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

    def display_scores(self):
        results = self._execute_command('SELECT name, win, game FROM user', tuple())
        result = ""
        for r in results:
            ratio = 0 if r[2] == 0 else r[1]/r[2]
            result += "Name: {}\t Win Ratio: {}\t\n".format(r[0], ratio)
        return result


    def _execute_command(self, command, args):
        cursor = self.db.cursor()
        cursor.execute(command, args)
        result = [r for r in cursor]
        cursor.close()
        return result

    def __exit__(self):
        self.db.commit()
        self.db.close()

    def update_game(self, players, winner):
        # winner is a list because in the event of a tie, nobody gets a win point
        print(players)
        for p in players:
            self._execute_command("UPDATE user SET game=(game + 1) WHERE name=?", (p,))
        for w in winner:
            print(w)
            self._execute_command("UPDATE user SET win=(win + 1) WHERE name=?", (w,))
        self.db.commit()

    def _hash(self, string):
        return hashlib.md5(string.encode('utf-8')).hexdigest()

    
# For Testing
if (__name__ == "__main__"):
    # Flip dislay depending on what you're testing
    display = True
    if display:
        db = Database_Connection("users.db")
        #db._execute_command("UPDATE user SET game=(game + 1) WHERE name=?", (test,))
        db.print_database()
        print(db.display_scores())
    else:
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
        db.update_game(["test", "ouroboros"], ["ouroboros"])
        db.print_database()
