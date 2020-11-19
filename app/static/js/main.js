document.addEventListener('visibilitychange', function () {
    if (!document.hidden && window.location.pathname !== "/album") {
        window.location.href = "http://nerdymusician.com";
    }
});