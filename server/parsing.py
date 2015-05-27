# Module that handles the encoding and decoding and reading that JS's
# WebSocket insists on using

import base64
import hashlib

class DisconnectionError(Exception):
    pass

def process_message_for_client(message):
    # Start with 129 to say it is a text message
    result = [129]
    start_message_byte = -1
    message_length = len(message)
    
    if (message_length < 126):
        start_message_byte = 2
        result.append(message_length)
    elif (message_length < 65536):
        start_message_byte = 4
        result.append(126)
        result.append((message_length >> 8) & 255)
        result.append((message_length) & 255)
    else:
        start_message_byte = 8
        result.append(127)
        for i in reversed(range(0, 57, 8)):
            result.append((message_length >> i) & 255)
    for char in message:
        result.append(ord(char))
    byte_result = bytes(result)
    return byte_result


def parse_message_from_client(message):
    # byte_list = ints that came from the 0's and 1's that were the message
    byte_list = [byte for byte in message]
    # !!!!! very very first byte may say if the message is done or not
    if byte_list[0] == 129:
        # Message is text
        pass
    elif (byte_list[0] == 136):
        # Client D/C. Will handle later,  most likely raise a custom error
        return "D/C"
    else:
        print(message)
        raise TypeError("Some other kind of message was received, number={}".format(byte_list[0]))

    # Removes first bit to get the message length
    # The first bit is supposed to say the message is encoded?
    # Which means it should be 0 when writing the reply to client
    # & is the python AND
    message_length = byte_list[1] & 0b01111111 

    # Since at least the first two bits are information, the message starts on byte 2 at earliest
    # If the message length was too long, more bytes are used for length and the masks starts
    # on byte 4 or 10 instead of 2
    first_message_byte = 2
    if (message_length == 0b01111110):
        # message_length = 126, next two bytes also define length of message
        first_message_byte = 4
    elif (message_length == 0b01111111):
        # byte_length = 127, next eight bytes also define length of message
        first_message_byte = 10

    # The four bytes after the length are masks
    masks = byte_list[first_message_byte: first_message_byte + 4]

    # First byte to decode starts after the masks
    result = ""
    counter = 0
    current_byte = first_message_byte + 4
    while current_byte < len(byte_list):
        # ^ is XOR
        # Ah, so the masks are kind of steam-roll-print applied to the rest
        # of the message to decode it
        result += chr(byte_list[current_byte] ^ masks[counter % 4])
        current_byte += 1
        counter += 1

    return result

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
    # Testing
    assert(parse_message_from_client(b'\x81\x82\x1b\x1b$\xdasr') == "hi")
    print(process_message_for_client("hello"))
