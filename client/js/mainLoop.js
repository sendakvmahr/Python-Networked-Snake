define(["physics/Vector", "input/Button", "scene/MainScene", "input/InputHandler","lib/goody", "assets/vars"],
function(Vector, Button, MainScene, InputHandler, goody, vars)
{
    function mainLoop() {
        this.canvas = document.getElementById('canvas');
        this.canvas.width = vars.displayWidth;
        this.canvas.height = vars.displayHeight;
        // Assign in main.js
        this.connection = "";
        this.input = new InputHandler.InputHandler(connection); 
        this.ctx = this.canvas.getContext('2d');
        /*
        this.scene = new MainScene.MainScene(
            [new Button.Button(images.food, 
                new Vector.Vector(520, 200), 
                function() {}
            )], 
            [images.snake]
        );
        */
        this.scene = new MainScene.MainScene();
        this.resizeCanvas();  
    };
    
    mainLoop.prototype.resizeCanvas = function() {
        
        this.draw();
    };
    
    mainLoop.prototype.updateInput = function(event) {   
        this.input.update(event, this.scene);
        // Change to connection
        // sending
    }; 
    
    mainLoop.prototype.updateFromServer = function(gameStateObject) {
        this.scene.loadScene(gameStateObject);
    }
    
    mainLoop.prototype.draw = function() {
        this.scene.display(this.ctx);
    };
    
    mainLoop.prototype.update = function() {
        /*
        if (this.scene.switchScenes) {
            this.scene = this.scene.nextScene();
        }
        this.scene.update(this.input);
        */
    };
    
    return {
        mainLoop : mainLoop
    };
});