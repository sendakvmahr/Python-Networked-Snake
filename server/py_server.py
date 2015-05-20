import threading
import time
import socket
import parsing
import database_handler

BUFFER_SIZE = 1024

class Client(threading.Thread):
    def __init__(self, socket, address):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self._game = ""
        self.message = ""
        self.logged_in = False
        self.start()
        
    def run(self):
        """Overwrites the Thread run function so it knows how to run"""
        while True:
            if (self.logged_in):
                # User has finished handshake and logged in
                # Either join / change movement / create game
                data = self._read_data()
                response = ""
            elif (self.socket in SERVER.clients.keys()):
                # Handshake is done
                data = self._read_data()
                response = ""
                if (data.startswith("login")):
                    userinfo = data.strip().split("\t")[1:]
                    response = self._handle_login(userinfo[0], userinfo[1])
                    print("LOGIN " + response + ": ", userinfo)
                elif (data.startswith("create")):
                    userinfo = data.strip().split("\t")[1:]
                    response = self._handle_create(userinfo[0], userinfo[1])
                    print("CREATE " + response + ": ", userinfo)
                else: 
                    # things that are left to implement - spectate, error
                    # spectate is not important for current milestone, it can wait
                    pass
                self._send(response)
                print("REPLIED : ", response)
            else:
                # Initial handshake
                self._handle_handshake()

    def _send(self, message):
        self.socket.send(parsing.process_message_for_client(message))

    def _read_data(self):
        return parsing.parse_message_from_client(self.socket.recv((BUFFER_SIZE)))

    def _handle_login(self, username, password):
        db = database_handler.Database_Connection("users.db")
        authenticated = db.authenticate_user(username, password)
        response = ""
        if (username in CLIENTS.keys()):
            response = "FAILURE: USER ALREADY LOGGED IN"
        elif (authenticated):
            response = "SUCCESS : USER LOGGED IN"
            self.logged_in = True
        else:
            response = "FAILURE: WRONG PASSWORD OR USERNAME"
        return response
    
    def _handle_create(self, username, password):
        db = database_handler.Database_Connection("users.db")
        authenticated = db.authenticate_user(username, password)
        response = ""
        could_create = db.create_user(username, password)
        if (could_create):
            response = "SUCCESS : USER CREATED AND LOGGED IN"
            self.logged_in = True
        else:
            response = "FAILURE: COULD NOT CREATE USER"
        return response

    def _handle_handshake(self):
        if (self.message.endswith("\n")):
            print("UNKNOWN SENT:", self.message)
            response = parsing.create_handshake_resp(self.message).encode('utf-8')
            self.socket.send(response)
            self.message = ""
            SERVER.clients[self.socket] = ""
        else:
            self.message += self.socket.recv((BUFFER_SIZE)).decode()


    
PORT = 11000

# If a message is bigger... I don't have a handler for that atm...Figure out if messages get that big

# Spectators and players who have not logged in
UNIDENTIFIED_CLIENTS = {}

# clients[game] = socket
CLIENTS = {}

class Server:
    def __init__(self, port):
        self._server_socket = socket.socket()
        self.port = port
        self._server_socket.bind(("127.0.0.1", self.port))
        self.clients = {}
        # self.clients[client_socket] = game_client_is_watching
        # if client is not watching a game, then game_client_is_watching is an empty string

        # Difference between clients that are signed in and aren't don't matter to the server - 
        # that is handled by the socket + thread watching each connection to the client
        # self.games[game_name] = networked_version_of_game
        self.games = {}

    def start(self):
        print("SERVER STARTED")
        self._server_socket.listen(20)
        while True:
            clientsocket, address = self._server_socket.accept()
            new_client = Client(clientsocket, address)
        
    def add_game(self, num_players):
        pass

if (__name__ == "__main__"):
    SERVER = Server(11000)
    SERVER.start()
