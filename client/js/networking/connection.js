function Connection(ip, port) {
        this.socket = new WebSocket("ws://" + ip + ":" + port.toString() + "/");
        // I don't think you have to define these,
        // I'll just leave this here in case I have to modify it later
        this.socket.onopen = function(evt) { console.log(evt) }; 
        this.socket.onclose = function(evt) { console.log(evt) }; 
        this.socket.onmessage = function(evt) { console.log(evt); }; //  I think it makes the most sense to override this in the... game loop class 
        this.socket.onerror = function(evt) { console.log(evt) };
}

Connection.prototype.send = function(input) {
    this.socket.send(input);
}

