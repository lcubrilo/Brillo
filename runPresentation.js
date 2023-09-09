define([
    'base/js/namespace',
    'base/js/events'
], function(Jupyter, events) {
    console.log("runPresentation.js loaded");

    function startSlideshow() {
        if (Jupyter && Jupyter.actions) {
            console.log("Attempting to start RISE slideshow");
            Jupyter.actions.call('rise:slideshow');
        } else {
            console.log("Jupyter actions not ready");
        }
    }

    // Listen for multiple events
    events.on("kernel_ready.Kernel", startSlideshow);
    events.on("notebook_loaded.Notebook", startSlideshow);
    events.on("rise:loaded", startSlideshow);
});
