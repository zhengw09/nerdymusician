document.addEventListener('visibilitychange', function () {
    if (document.hidden) {
        window.location.href = "http://nerdymusician.com";
        document.getElementById("demo").innerHTML = "show";
    }
});