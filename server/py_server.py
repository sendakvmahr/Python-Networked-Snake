import threading
import time
import socket
import parsing
import database_handler
import snake_logic

# 1/FPS instead of 1000/FPS 'cause sleep takes time input in seconds
FPS = 30
SLEEP = 3/FPS
BUFFER_SIZE = 1024

class Networked_Game(threading.Thread):
    def __init__(self, name, num_players):
        threading.Thread.__init__(self)
        self.name = name
        self.started = False
        self.num_players = num_players
        # self.players[player_name] = player_socket
        self.players = {}
        self._game_state = ""
        
    def run(self):
        # This needs to stop when the game is over
        while True:
            self._game_state.update()
            update = self._game_state.to_JSON()
            print(update)
            update = parsing.process_message_for_client(update)
            for player in self.players.keys():
                self.players[player].send(update)
            time.sleep(SLEEP)
            
    def join(self, player_name, socket):
        self.players[player_name] = socket
        if (self.num_players == len(self.players)):
            self._game_state = snake_logic.Game_State([p for p in self.players.keys()])
            self.start()
        print("{}.started = {}".format(self.name, self.started))

class Client(threading.Thread):
    def __init__(self, socket, address):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self._game = ""
        self._username = ""
        self.message = ""
        self.logged_in = False
        self.start()
        
    def run(self):
        """Overwrites the Thread run function so it knows how to run"""
        while True:
            ### NOTES ON WHAT IS NOT IMPLEMENTED
            # logged in - processing moves, though that has more to do wiht the client atm
            # anyone - disconnections
            # spectate option
            # request_games shouldn't be there, server should update everyone on the state of the games when they change
            if (self.logged_in):
                # User has finished handshake and logged in
                # Either join / change movement / create game
                data = self._read_data()
                response = ""
                print(data)
                if (data.startswith("create")):
                    data = self._split_message(data)
                    game_name = data[0]
                    num_players = int(data[1])
                    SERVER.add_game(game_name, num_players)
                    SERVER.join(game_name, self._username, self.socket)
                elif (data.startswith("move")):
                    #self._game.update_player_direction(self._user, self._split_message(data)[0])
                    pass
                elif (data.startswith("join")):
                    game_name = self._split_message(data)[0]
                    SERVER.join(game_name, self._username, self.socket)
                elif (data.startswith("request_games")):
                    response = SERVER.games.items()
                    
            elif (self.socket in SERVER.clients.keys()):
                # Handshake is done
                data = self._read_data()
                response = ""
                if (data.startswith("login")):
                    userinfo = self._split_message(data)
                    response = self._handle_login(userinfo[0], userinfo[1])
                    print("LOGIN " + response + ": ", userinfo)
                elif (data.startswith("create")):
                    userinfo = self._split_message(data)
                    response = self._handle_create(userinfo[0], userinfo[1])
                    print("CREATE " + response + ": ", userinfo)
                elif (data.startswith("request_games")):
                    response = SERVER.games.items()
                    # things that are left to implement - spectate, error
                self._send(response)
                print("REPLIED : ", response)
            else:
                # Initial handshake
                self._handle_handshake()

    def _split_message(self, message):
        # Takes out the first part of the response, leaves the "arguments" for the client
        return message.strip().split("\t")[1:]

    def _send(self, message):
        self.socket.send(parsing.process_message_for_client(message))

    def _read_data(self):
        return parsing.parse_message_from_client(self.socket.recv((BUFFER_SIZE)))

    def _handle_login(self, username, password):
        db = database_handler.Database_Connection("users.db")
        authenticated = db.authenticate_user(username, password)
        response = ""
        if (username in SERVER.clients):
            response = "FAILURE: USER ALREADY LOGGED IN"
        elif (authenticated):
            response = "SUCCESS : USER LOGGED IN"
            self._username = username
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
            self._username = username
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

        # !!!!! I have a feeling there needs to be a threading lock on self.games and self.clients soon...
        self.games = {}

    def start(self):
        print("SERVER STARTED")
        self._server_socket.listen(20)
        while True:
            clientsocket, address = self._server_socket.accept()
            new_client = Client(clientsocket, address)
        
    def add_game(self, game_name, num_players):
        if (game_name not in self.games.keys()):
            self.games[game_name] = Networked_Game(game_name, num_players)
        
    def join(self, game_name, username, socket):
        self.games[game_name].join(username, socket)
        

if (__name__ == "__main__"):
    SERVER = Server(11000)
    SERVER.start()
