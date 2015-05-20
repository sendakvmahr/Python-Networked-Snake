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
                try {
                    gameState = JSON.parse(evt.data);
                    //console.log(gameState)
                    main.updateFromServer(gameState);
                    main.draw();
                }
                catch(err) {
                    console.log(err)
                }
            };
            // should pass connection socket
            /*
            window.requestAnimationFrame(start);
            currentTime = (new Date()).getTime();
            timeDelta = currentTime - lastTime;
            if (timeDelta > vars.interval) 
            {
                main.update(); 
                timeDelta = 0;           
                lastTime = currentTime;
            }
            */
        }
        start(connection);
    });
}
