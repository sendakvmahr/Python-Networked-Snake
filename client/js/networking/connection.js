function Connection(ip, port) {
        this.socket = new WebSocket("ws://" + ip + ":" + port.toString() + "/");
        // Shakey and if I change connection to another name it dies...
        this.socket.onopen = function(evt) { console.log(evt);
                                             start(connection)
                                             }; 
        this.socket.onclose = function(evt) { console.log(evt) }; 
        this.socket.onmessage = function(evt) { console.log(evt) };
        this.socket.onerror = function(evt) { console.log(evt) };
}

Connection.prototype.send = function(input) {
    this.socket.send(input);
}

