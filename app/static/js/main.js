document.addEventListener('visibilitychange', function () {
    if (window.location.pathname !== "/album") {
        window.location.href = "http://nerdymusician.com";
    }
});