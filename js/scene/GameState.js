define([],
function()
{    
    function GameState() {
        this.drawSnakes = [];
        this.snakeHeads = {};
        this.drawFood = [];
        // Thinking about it I think the server can tell which player it is haha
        this.player = "";
        this.score = [0, 0];
    }

    GameState.prototype.load = function(gameStateObject) {
        // var test = JSON.stringify(this);
        // console.log(test);
        // var newState = JSON.parse(messageFromServer);
        // var newState = JSON.parse(test);
        var newState = gameStateObject;
        this.drawSnakes = newState.drawSnakes;
        console.log(this.drawSnakes);
        this.drawFood = newState.drawFood;
        this.player = newState.player;
        this.score = newState.score;
    }

    return {
        GameState:GameState
    };
});