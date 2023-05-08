/* make console text copiable */
new ClipboardJS('.console', {
    text: function (trigger) {
        return trigger.innerText;
    }
}).on('success', function (e) {
    const evt = e.trigger;
    evt.classList.add('copied')
    setTimeout(function () {
        evt.classList.remove('copied');
    }, 1500)
});