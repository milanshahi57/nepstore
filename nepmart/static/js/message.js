document.addEventListener("DOMContentLoaded", function() {
    let popup = document.getElementById("popup-message");
    if (popup) {
        popup.classList.add("show");
        setTimeout(function() {
            popup.classList.remove("show");
        }, 3000);
    }
});
