define([],
function()
{    
    function Scene() {
        this.switchScenes = false;
    }

    Scene.prototype.update = function(input, delta) {
    }

    Scene.prototype.click = function(mousePosition) {
    }

    Scene.prototype.rightClick = function(mousePosition) {
    }

    Scene.prototype.display = function(ctx) {
    }

    Scene.prototype.nextScene = function() {
        if (!this.switchScenes) {
            throw new Error("switchScenes is false");
        }
    }

    return {
        Scene:Scene
    };
});