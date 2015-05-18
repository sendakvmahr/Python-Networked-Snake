define(["physics/Rect", "physics/Vector"],
function(Rect, Vector)
{    
    function Button(image, location, clickFunction) {
        this.clickFunction = clickFunction;
        this.image = image;
        this.offsetImage = new Vector.Vector(0,0);
        this.hover = false;
        this.rect = new Rect.Rect(location.x, location.y, image.width, image.height);
    }

    Button.prototype.contains = function(Vector) {
        return this.rect.collideVector(Vector);
    }
    
    Button.prototype.display = function(ctx) {
        ctx.drawImage (
            this.image,                                                  //image
            this.offsetImage.x,                                          //x position on image
            this.offsetImage.y,                                          //y position on image
            this.image.width,                                            //imageWidth on Source
            this.image.height,                                           //imageHeight on Source
            this.rect.position.x,                                        //xPosCanvas    
            this.rect.position.y,                                        //yPosCanvas, integer offsets are for centering  
            this.rect.width,                                             //imageWidth on Canvas
            this.rect.height                                             //imageHeight on Canvas                
        );
    }

    return {
        Button: Button
    };
});