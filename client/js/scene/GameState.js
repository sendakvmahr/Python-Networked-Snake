define([],
function()
{    
    function GameState() {
        this.drawSnakes = [[50, 50], [40, 50],  [80, 80]];
        this.snakeHeads = {
            "player1" : [50, 50],
            "player2" : [80, 80]
        }
        this.drawFood = [30, 30];
        // Thinking about it I think the server can tell which player it is haha
        this.player = "";
        this.score = [0, 0];
    }

    GameState.prototype.load = function(messageFromServer) {
        var test = JSON.stringify(this);
        console.log(test);
        // var newState = JSON.parse(messageFromServer);
        var newState = JSON.parse(test);
        this.drawSnakes = newState.drawSnakes;
        this.drawFood = newState.drawFood;
        this.player = newState.player;
        this.score = newState.score;
    }

    return {
        GameState:GameState
    };
});