define([
    'base/js/namespace',
    'base/js/events'
], function(Jupyter, events) {
    events.on("kernel_ready.Kernel", function () {
        Jupyter.actions.call('rise:slideshow');
    });
});
