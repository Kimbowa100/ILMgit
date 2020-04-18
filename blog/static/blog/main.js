$("#pop").on("click", function() {
    $('#imagepreview').attr('src', $('#imageresource').attr('src')); // here asign the image to the modal when the user click the enlarge link
    $('#imagemodal').modal('show'); // imagemodal is the id attribute assigned to the bootstrap modal, then i use the show function
});
var state = 'stop';

function buttonBackPress() {
    console.log("button back invoked.");
}

function buttonForwardPress() {
    console.log("button forward invoked.");
}

function buttonRewindPress() {
    console.log("button rewind invoked.");
}

function buttonFastforwardPress() {
    console.log("button fast forward invoked.");
}

function buttonPlayPress() {
    if (state == 'stop') {
        state = 'play';
        var button = d3.select("#button_play").classed('btn-success', true);
        button.select("i").attr('class', "fa fa-pause");
    } else if (state == 'play' || state == 'resume') {
        state = 'pause';
        d3.select("#button_play i").attr('class', "fa fa-play");
    } else if (state == 'pause') {
        state = 'resume';
        d3.select("#button_play i").attr('class', "fa fa-pause");
    }
    console.log("button play pressed, play was " + state);
}

function buttonStopPress() {
    state = 'stop';
    var button = d3.select("#button_play").classed('btn-success', false);
    button.select("i").attr('class', "fa fa-play");
    console.log("button stop invoked.");
}
