document.addEventListener('visibilitychange', function () {
    if (document.hidden) {
        document.getElementById("demo").innerHTML = "Hidden";
    } else {
        document.getElementById("demo").innerHTML = "Shown";
    }
});