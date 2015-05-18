import threading
import base64
import hashlib
import time
import socket
import parsing

PORT = 11000
LOCK = threading.Lock()
BUFFER_SIZE = 1024 # If a message is bigger... I don't have a handler for that atm...Figure out if the states get that big
UNIDENTIFIED_CLIENTS = []
IDENTIFIED_CLIENTS = []
CLIENTS = {}

class Client(threading.Thread):
    def __init__(self, socket, address):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.message = ""
        self.start()

    def run(self):
        """My brain is dead right now, "overwrites" the Thread run function"""
        while True:
            if (self.socket in UNIDENTIFIED_CLIENTS):
                # Handshake is done
                # Either login / create / spectate
                data = parsing.parse_message_from_client(self.socket.recv((BUFFER_SIZE)))
                if (data.startswith("login")):
                    userinfo = data.strip().split("\t")[1:]
                    print("LOGIN: ", userinfo)
                elif (data.startswith("create")):
                    userinfo = data.strip().split("\t")[1:]
                    print("CREATE: ", userinfo)
                else:
                    # things that are left to implement - spectate, error 
                    pass
                # Echo for now
                self.socket.send(parsing.process_message_for_client(data))
                print("UNIDENTIFIED CLIENT SENT: ", data)
                print("REPLIED : ", data)
                
                print(UNIDENTIFIED_CLIENTS)
            elif (self.socket in IDENTIFIED_CLIENTS):
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
                    UNIDENTIFIED_CLIENTS.append(self.socket)
                else:
                    self.message += self.socket.recv((BUFFER_SIZE)).decode()
            
class Server:

    def __init__(self, port):
        self._server_socket = socket.socket()
        self._port = port
        self._server_socket.bind(("127.0.0.1", self._port))
        self.lock = threading.Lock()

    def start(self):
        print("SERVER STARTED")
        self._server_socket.listen(20)
        while True:
            clientsocket, address = self._server_socket.accept()
            new_client = Client(clientsocket, address)
            

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
