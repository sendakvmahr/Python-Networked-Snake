var imageNames = [
    "food",
    "snake"
]
var ip;
var connection;
var username;
var images = {};
var canStart = false;

$(function() {  
    $("#connect-button").on("click",  function(event) {
        // Just connects to the server - ideally, this would be automatic, but
        // I do not have a static IP so this has to be manually done
        ip = $("#ip-field").val();
        //console.log(ip);
        connection = new Connection(ip, "11000");
        //console.log(connection);
        
    });
    
    $("#login-button").on("click", function(event){
        try {
            //console.log("Logging in");
            username = $("#username").val();
            var password = $("#password").val();
            connection.send("login:\t" + username + "\t" + password + "\n");
        }
        catch(error) {
            console.log(error);
        }
    });

    $("#create-button").on("click", function(event){
        try {
            console.log("Creating user");
            username = $("#username").val();
            var password = $("#password").val();
            connection.send("create:\t" + username + "\t" + password + "\n");
        }
        catch(error) {
            console.log(error);
        }
    });
    
    $("#create-game-button").on("click", function(event){
        try {
            console.log("Creating game");
            var game = $("#game_name").val();
            var num_players = $("#player_num").val().toString();
            connection.send("create:\t" + game + "\t" + num_players);
        }
        catch(error) {
            console.log(error);
        }
    });
    
    $("#join-game-button").on("click", function(event){
        try {
            console.log("Joining game");
            var game = $("#game_name").val();
            connection.send("join:\t" + game);
        }
        catch(error) {
            console.log(error);
        }
    });
    
    
    $("#request-games-button").on("click", function(event){
        try {
            connection.send("request_games");
        }
        catch(error) {
            console.log(error);
        }
    });
    
    
    $("#request-scores-button").on("click", function(event){
        try {
            connection.send("request_scores");
        }
        catch(error) {
            console.log(error);
        }
    });
    
    // functions I've been using in the console that should be attatched to buttons
    /*
    
    
                #create-game-button{
                float: left;
                margin-left: .7rem;
            }
            #join-game-button{
                float: right;
                margin-right: .7rem;
            }
    connection.send("create:\tnewgame\t2")
    connection.send("create:\tnewgame2\t3")
    connection.send("join:\tnewgame")
    */
    
    // Load all the images
    var loaded = 0;
    var numImages = imageNames.length;
    if (imageNames.length == 0) {
        start();
    }
    else {
        for (var i = 0; i < numImages; i++) {
            var index = imageNames[i];
            images[index] = new Image();
            images[index].src = "images/" + index + ".png";
            images[index].onload = function(){ 
                loaded++;
                if (loaded === numImages) {
                    canStart = true;
                } 
            }
        }
    }
});
