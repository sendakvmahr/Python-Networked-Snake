define(["lib/goody"],
function(goody)
{    
    function Vector(x, y, z){
        // Used for direction and position
        this.x = goody.optional(x, 0);
        this.y = goody.optional(y, 0);
        this.z = goody.optional(z, 0);
    };

    Vector.prototype.add = function(Vector2){
        // Adds two Vectors together, returns a new Vector
        return new Vector(this.x + Vector2.x, this.y + Vector2.y, this.z + Vector2.z);
    };

    Vector.prototype.mult = function(i) {
        // Multiplies the entire vector by i. 
        // Useful for friction
        this.x = this.x * i;
        this.y = this.y * i;
        this.z = this.z * i;
    };

    Vector.prototype.length = function() {
        // Magnitude of the vector
        var x = this.x;
        var y = this.y;
        var z = this.z;
        return Math.sqrt(x * x + y * y + z * z);
    };

    Vector.prototype.setLength = function(len) {
        // Sets the magnitude of the vector
        var currentLength = this.length();
        this.x = this.x * len / currentLength;
        this.y = this.y * len / currentLength;
        this.z = this.z * len / currentLength;
    };

    Vector.prototype.getDirection = function() {
        return Math.atan2(this.y, this.x);
    }
    
    return {
        Vector: Vector
    };
});