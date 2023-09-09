define([
    'base/js/namespace',
    'base/js/events'
], function(Jupyter, events) {
    console.log("runPresentation.js loaded");  // Debug statement
    events.on("kernel_ready.Kernel", function () {
        Jupyter.actions.call('rise:slideshow');
    });
});
