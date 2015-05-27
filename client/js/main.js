function start(connection) {
    require(["mainLoop", "assets/vars"],
    function(mainLoop, vars) 
    {    
        var main = new mainLoop.mainLoop(connection);
        function resize() { main.resizeCanvas(); }
        function ev(event) { main.updateInput(event); }
        
        console.log(main.updateInput);
        var $canvas = $("#canvas");
        $canvas.bind("contextmenu mousemove click", ev);

        $(document).keyup(function(e) { ev(e); });
        $(document).keydown(function(e) { ev(e); });
        
        window.addEventListener('resize', resize);
        
        // not sure what this does, research later
        var vendors = ['webkit', 'moz'];
        for (var x = 0; x < vendors.length && !window.requestAnimationFrame; ++x) {
            window.requestAnimationFrame = window[vendors[x] + 'RequestAnimationFrame'];
            window.cancelAnimationFrame = window[vendors[x] + 'CancelAnimationFrame'] || window[vendors[x] + 'CancelRequestAnimationFrame'];
        }

        var lastTime = (new Date()).getTime();
        var currentTime = 0;
        var timeDelta = 0;

        function start(connection) {    
            connection.socket.onmessage = function(evt) { 
                console.log(evt.data);
                if (evt.data.startsWith("GAMES")) {
                    var data = evt.data.replace("\t", ":").replace("[", "").replace("]", "");
                    $("#info").html(data);
                }
                else if (evt.data.startsWith("SCORES")) {
                    var data = evt.data.replace("\t", ":<br/>").replace("[", "").replace("]", "").replace("\n", "<br/>");
                    $("#info").html(data);
                }
                try {
                    if (evt.data[0] == "{") {
                        gameState = JSON.parse(evt.data);
                        //console.log(gameState)
                        main.updateFromServer(gameState);
                        main.draw();
                    }
                }
                catch(err) {
                    console.log(err)
                }
            };
        }
        start(connection);
    });
}
