define(["lib/goody", "physics/Vector"],
function(goody, Vector)
{    
    function Rect(x, y, width, height){
        this.position = new Vector.Vector(x, y);
        this.width = width;
        this.height = height;
    };

    // General useful functions
    Rect.prototype.getLeft = function() { return this.position.x; };
    Rect.prototype.getRight = function() { return this.position.x + this.width; };
    Rect.prototype.getTop = function() { return this.position.y; };
    Rect.prototype.getBottom = function() { return this.position.y + this.height; };
    
    Rect.prototype.setLeft = function(x) { this.position.x = x; };
    Rect.prototype.setRight = function(x) { this.position.x = x - this.width; };
    Rect.prototype.setTop = function(y) { this.position.y = y; };
    Rect.prototype.setBottom = function(y) { this.position.y = y - this.height; };
    
    Rect.prototype.center = function() { return Vector.Vector(this.position.x + Math.floor(this.width/2), this.position.y + Math.floor(this.height/2)); }; 
    Rect.prototype.collideRect = function(r2) { return !(this.getLeft() > r2.getRight() || this.getRight() < r2.getLeft() || this.getTop() > r2.getBottom() || this.getBottom() < r2.getTop()); };
    Rect.prototype.collideVector = function(p) { return (p.x > this.getLeft() && p.x < this.getRight() && p.y < this.getBottom() && p.y > this.getTop()); };
    
    Rect.prototype.getCorners = function() { 
    // Upper Left, Upper Right, Lower Left, Lower Right
        return [
            new Vector.Vector(this.position.x, this.position.y),
            new Vector.Vector(this.position.x + this.width, this.position.y),
            new Vector.Vector(this.position.x, this.position.y + this.height),
            new Vector.Vector(this.position.x + this.width, this.position.y + this.height),
        ];
    }
    
    Rect.prototype.draw = function(ctx, offset, color) {
        // Draws the rect on a canvas context
        ctx.fillStyle = goody.optional(color, (Math.random().toString(16) + '000000').slice(2, 8));
        ctx.fillRect(this.position.x + offset.x, this.position.y + offset.y, this.width, this.height);
    }
    
    return {
        Rect: Rect
    };
});