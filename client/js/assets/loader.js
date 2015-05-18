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
        console.log(ip);
        connection = new Connection(ip, "11000");
        console.log(connection);
        // Should trigger spectator state, if can implement in time
    });

    $("#login-button").on("click", function(event){
        try {
            console.log("Logging in");
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
