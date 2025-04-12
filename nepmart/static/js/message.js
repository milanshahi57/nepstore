document.addEventListener("DOMContentLoaded", function() {
    // Handle popup messages
    let popup = document.getElementById("popup-message");
    if (popup) {
        popup.classList.add("show");
        setTimeout(function() {
            popup.classList.remove("show");
        }, 3000);
    }

    // Handle Django messages
    let alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.classList.add('hide');
            setTimeout(function() {
                alert.remove();
            }, 500);
        }, 3000);
    });
});
