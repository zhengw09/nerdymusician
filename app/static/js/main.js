document.addEventListener('visibilitychange', function () {
    if (window.location.pathname !== "/album") {
        window.location.href = "http://nerdymusician.com";
    }
});

var textNode = document.getElementById("msgs");
console.log(textNode);
textNode.innerHTML = textNode.innerHTML.replace(/(https?:\/\/[^\s]+)/g, "<a href='$1'>$1</a>");