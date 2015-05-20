import threading
import base64
import hashlib
import time
import socket
import parsing
import database_handler

PORT = 11000
# I'm not sure if I'll need this later, we'll see
# LOCK = threading.Lock()

# If a message is bigger... I don't have a handler for that atm...Figure out if messages get that big
BUFFER_SIZE = 1024

# This is a mess

# Spectators, mainly
UNIDENTIFIED_CLIENTS = {}

CLIENTS = {}


class Client(threading.Thread):
    def __init__(self, socket, address):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.message = ""
        self.logged_in = False
        self.start()
        
    def _handle_login(self, username, password):
        db = database_handler.Database_Connection("users.db")
        authenticated = db.authenticate_user(username, password)
        response = ""
        if (username in CLIENTS.keys()):
            response = "FAILURE: USER ALREADY LOGGED IN"
        elif (authenticated):
            response = "SUCCESS"
            self.logged_in = True
            CLIENTS[username] = self.socket
        else:
            response = "FAILURE: WRONG PASSWORD OR USERNAME"
        return response
    
    def _handle_create(self, username, password):
        db = database_handler.Database_Connection("users.db")
        authenticated = db.authenticate_user(username, password)
        response = ""
        could_create = db.create_user(username, password)
        if (could_create):
            response = "USER CREATED AND LOGGED IN"
            self.logged_in = True
            CLIENTS[username] = self.socket
        else:
            response = "FAILURE: COULD NOT CREATE USER"
        return response
        
    def run(self):
        """My brain is dead right now, "overwrites" the Thread run function so it knows how to run"""
        while True:
            if (self.socket in UNIDENTIFIED_CLIENTS.keys()):
                # Handshake is done
                data = parsing.parse_message_from_client(self.socket.recv((BUFFER_SIZE)))
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
                    pass
                self.socket.send(parsing.process_message_for_client(response))
                print("REPLIED : ", response)
            elif (self.logged_in):
                # User has finished handshake and logged in
                # Either join / change movement
                pass
            else:
                # Initial handshake
                if (self.message.endswith("\n")):
                    print("UNKNOWN SENT:", self.message)
                    response = create_handshake_resp(self.message).encode('utf-8')
                    self.socket.send(response)
                    self.message = ""
                    print("END HANDSHAKE")
                    UNIDENTIFIED_CLIENTS[self.socket] = ""
                else:
                    self.message += self.socket.recv((BUFFER_SIZE)).decode()
            
class Server:

    def __init__(self, port):
        self._server_socket = socket.socket()
        self._port = port
        self._server_socket.bind(("127.0.0.1", self._port))

    def start(self):
        print("SERVER STARTED")
        self._server_socket.listen(20)
        while True:
            clientsocket, address = self._server_socket.accept()
            new_client = Client(clientsocket, address)
            

# Shouldn't this be in parser...? it feels like it should be but things would have to be renamed
def create_handshake_resp(handshake):
    # Some string that is used everywhere for this
    specificationGUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    websocketKey = ''

    # Parsing handshake request
    lines = handshake.splitlines()
    for line in lines:
            args = line.partition(": ")
            if args[0] == 'Sec-WebSocket-Key':
                    websocketKey = args[2]
                    
    concatenate_keys = (websocketKey + specificationGUID).encode()
    full_key = hashlib.sha1(concatenate_keys).digest()
    accept_key = base64.b64encode(full_key)
    accept_key_string = accept_key.decode()

    return 'HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: ' + accept_key_string + '\r\n\r\n'


if (__name__ == "__main__"):
    s = Server(PORT)
    s.start()
