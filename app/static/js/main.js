document.addEventListener('visibilitychange', function () {
    if (document.visible) {
        window.location.href = "http://nerdymusician.com";
        document.getElementById("demo").innerHTML = "show";
    }
});