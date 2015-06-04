define(["scene/GameState", "assets/vars"],
function(GameState, vars)
{    
    function MainScene() {
        this.gameState = new GameState.GameState();
    }
    
    MainScene.prototype.loadScene = function(jsonData) {
        this.gameState.load(jsonData);
    }

    MainScene.prototype.update = function(input, delta) {
        /*
        atually not called
        for (var i = 0; i < this.buttons.length; i++) { 
            if (this.buttons[i].contains(input.mousePosition)) {
                this.buttons[i].hover = true; // need a place where this is set to false
            }
        }
        */
    }

    MainScene.prototype.click = function(mousePosition) {
        /*
        for (var i = 0; i < this.buttons.length; i++) {
            if (this.buttons[i].contains(mousePosition)) { 
                this.buttons[i].clickFunction(this);
            }
        } 
        */        
    }
    
    MainScene.prototype.drawImage = function(image, x, y, ctx) {
        ctx.drawImage(
            image,                                                      //image
            0,                                                          //x position on image
            0,                                                          //y position on image
            image.width,                                                //imageWidth on Source
            image.height,                                               //imageHeight on Source
            x,                                                          //xPosCanvas    
            y,                                                          //yPosCanvas    
            image.width,                                                //imageWidth on Canvas
            image.height                                               //imageHeight on Canvas        
        );
    }

    MainScene.prototype.display = function(ctx) {
        // Background
        ctx.fillStyle = vars.backgroundColor;
        ctx.fillRect(0, 0, vars.displayWidth, vars.displayHeight);
        // Snakes
        for (var i = 0; i < this.gameState.drawSnakes.length; i++) {
            this.drawImage(images.snake, this.gameState.drawSnakes[i][0], this.gameState.drawSnakes[i][1], ctx);
        }
        
        this.drawImage(images.food, this.gameState.drawFood[0], this.gameState.drawFood[1], ctx);

        
        // Borders 
        ctx.fillStyle = vars.borderColor;
        ctx.fillRect(0, 0, vars.displayWidth, vars.tileHeight);
        ctx.fillRect(0, vars.displayHeight - vars.tileHeight, vars.displayWidth, vars.tileHeight);
        ctx.fillRect(0, 0, vars.tileHeight, vars.displayHeight);
        ctx.fillRect(vars.displayWidth - vars.tileHeight, 0, vars.tileHeight, vars.displayHeight);
    }

    return {
        MainScene: MainScene
    };
});