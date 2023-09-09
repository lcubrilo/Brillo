define([
    'base/js/namespace',
    'base/js/events'
], function(Jupyter, events) {
    console.log("runPresentation.js loaded");  // Debug statement

    function startSlideshow() {
        Jupyter.actions.call('rise:slideshow');
    }

    events.on("kernel_ready.Kernel", startSlideshow);
    events.on("notebook_loaded.Notebook", startSlideshow);
});
