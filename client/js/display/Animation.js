define(["physics/Vector", "lib/goody", "assets/vars"],
function(Vector, goody, vars)
{    
    function Animation(image, frames, width, height) {
        this.width = width;
        this.height = height;
        this._maxFrames = frames;
        this._frame = 0;
        this._image = image;
        this._imageOffset = new Vector.Vector(0, 0);
    }

    Animation.prototype.orient = function(direction) {
        // Mainly used for rotating sprites at the moment
        this._imageOffset.y = this.height * vars.directions[direction];
    }

    Animation.prototype.setOffsetY = function(y) {
        this._imageOffset.y = y;
    }
    
    Animation.prototype.update = function() {
        // Changes to the next frame and loops if needed
        this._frame = goody.incrementLoop(this._frame, this._maxFrames);
        this._imageOffset.x = this._frame * this.width;
    }
    
    Animation.prototype.display = function(ctx, offset){
        // Draws the current sprite
        ctx.drawImage(   
            this._image,                                                      //image
            this._imageOffset.x,                                              //x position on image
            this._imageOffset.y,                                              //y position on image
            this.width,                                                 //imageWidth on Source
            this.height,                                                //imageHeight on Source
            Math.floor(offset.x),                                                   //xPosCanvas    
            Math.floor(offset.y),                                                   //yPosCanvas, integer offsets are for centering  
            this.width,                                                 //imageWidth on Canvas
            this.height                                                 //imageHeight on Canvas                
        )
    }

    return {
        Animation:Animation
    };
});