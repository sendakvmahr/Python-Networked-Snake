define([],
function()
{

    // FPS is used in interval calculations, defined here
    var fps = 30;

    return {
        displayHeight: 500,
        displayWidth: 750,
        mapLength: 144,
        tileHeight: 10,
        fps: 30,
        interval: 1000/fps,
        borderColor: "#FFFFFF",
        backgroundColor: "#000000"
    }
});
