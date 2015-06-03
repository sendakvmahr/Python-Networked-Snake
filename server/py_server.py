import threading
import time
import socket
import parsing
import database_handler
import snake_logic
import json

# 1/FPS instead of 1000/FPS 'cause sleep takes time input in seconds
# OMG slow down the message rate and do prediction haha...
FPS = 15
SLEEP = 1/FPS
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
        while not self._game_state.finished:
            self._game_state.update()
            update = self._game_state.to_JSON()
            #print(update)
            update = parsing.process_message_for_client(update)
            for player in self.players.keys():
                self.players[player].send(update)
            time.sleep(SLEEP)
        db = database_handler.Database_Connection("users.db")
        winners = self._game_state.get_winners()
        db.update_game(list(self.players.keys()), winners)
        print(list(self.players.keys()), winners)
        message = parsing.process_message_for_client("WINNERS = {}".format(winners))
        for player in self.players.keys():
            self.players[player].send(message)
        print(message)
        SERVER.delete_game(self.name)        
            
    def join(self, player_name, socket):
        if (self.started):
            raise ValueError
        self.players[player_name] = socket
        if (self.num_players == len(self.players)):
            self._game_state = snake_logic.Game_State([p for p in self.players.keys()])
            self.started = True
            self.start()
        print("{}.started = {}".format(self.name, self.started))
    def update_player_direction(self, username, direction):
        self._game_state.update_player_direction(username, direction)

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

    def is_in_game(self):
        return type(self._game) != str
    def run(self):
        """Overwrites the Thread run function so it knows how to run"""
        while True:
            ### NOTES ON WHAT IS NOT IMPLEMENTED
            if (self.logged_in):
                # User has finished handshake and logged in
                # Either join / change movement / create game
                data = self._read_data()
                response = ""
                print(data)
                if (data.startswith("create")):
                    try:
                        data = self._split_message(data)
                        game_name = data[0]
                        num_players = int(data[1])
                        if (num_players > 1 and num_players < 5):
                            SERVER.add_game(game_name, num_players)
                            SERVER.join(game_name, self._username, self.socket)
                            self._game = SERVER.games[game_name]
                        self._send("CREATED")
                    except:
                        # Player did not enter a number for number of players or left something blank
                        self._send("ERROR: CHECK FIELDS")
                elif (data.startswith("dir") and self.is_in_game()):
                    self._game.update_player_direction(self._username, self._split_message(data)[0])
                elif (data.startswith("join") and not self.is_in_game()):
                    try:
                        game_name = self._split_message(data)[0]
                        joined = SERVER.join(game_name, self._username, self.socket)
                        if joined:
                            self._game = SERVER.games[game_name]
                            self._send("JOINED")
                        else:
                            self._send("ERROR: CHECK FIELDS")
                    except:
                        # Most likely they forgot to fill in a form
                         self._send("ERROR: CHECK FIELDS")
                elif (data.startswith("request_games")):
                    response = "GAMES\t" + self.get_games()
                    self._send(response)
                elif (data.startswith("request_scores")):
                    response = "SCORES\t" + self.get_scores()
                    self._send(response)
                elif (data == "D/C"):
                    del SERVER.clients[self.socket]
                    return
                print("REPLIED : ", response)
            elif (self.socket in SERVER.clients.keys()):
                # Handshake is done
                data = self._read_data()
                response = ""
                if (data.startswith("login")):
                    try:
                        userinfo = self._split_message(data)
                        response = self._handle_login(userinfo[0], userinfo[1])
                        print("LOGIN " + response + ": ", userinfo)
                    except:
                        # Most likely they forgot to fill in a form
                        pass
                elif (data.startswith("create")):
                    try:
                        userinfo = self._split_message(data)
                        response = self._handle_create(userinfo[0], userinfo[1])
                        print("CREATE " + response + ": ", userinfo)
                    except:
                        # Most likely they forgot to fill in a form
                        pass
                elif (data.startswith("request_games")):
                    response = "GAMES\t" + self.get_games()
                elif (data.startswith("request_scores")):
                    response = "SCORES\t" + self.get_scores()
                elif (data == "D/C"):
                    del SERVER.clients[self.socket]
                    return
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
        try:
            return parsing.parse_message_from_client(self.socket.recv((BUFFER_SIZE)))
        except:
            return ""

    def get_scores(self):
        db = database_handler.Database_Connection("users.db")
        return db.display_scores()

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
    def get_games(self):
        return str(list(SERVER.games.keys()))

class Server:
    def __init__(self, port):
        self._server_socket = socket.socket()
        self.port = port
        self._server_socket.bind(("0.0.0.0", self.port))
        self.clients = {}
        # self.clients[client_socket] = game_client_is_watching
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
        try:
            self.games[game_name].join(username, socket)
            return True
        except KeyError:
            # Game does not exist
            return False
        except ValueError:
            # Game has already started and has enough players
            return False
        
    def delete_game(self, game_name):
        del self.games[game_name]
    
        
if (__name__ == "__main__"):
    SERVER = Server(11000)
    SERVER.start()
