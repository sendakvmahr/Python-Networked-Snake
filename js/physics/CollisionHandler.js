define(["lib/goody"],
function(goody)
{    
    function CollisionHandler() {}

    CollisionHandler.prototype.collidingTiles = function(map, rect) {
        // Given a rect, find out which tiles it is on
        var points = rect.getCorners();
        var result = [];
        for (var i=0; i<4; i++) {
            var tile = map.pixelToTile(points[i]);
            if (!goody.inArray(result, tile)) {
                 result.push(tile);
            }
        }
        return result;
    }
    
    return {
        CollisionHandler: CollisionHandler
    };
});