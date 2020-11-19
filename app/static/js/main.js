document.addEventListener('visibilitychange', function () {
    if (document.visible && window.location.pathname !== "/album") {
        window.location.href = "http://nerdymusician.com";
    }
});
