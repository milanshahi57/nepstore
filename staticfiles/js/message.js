document.addEventListener("DOMContentLoaded", function() {
    // Handle popup messages
    let popup = document.getElementById("popup-message");
    if (popup) {
        popup.classList.add("show");
        setTimeout(function() {
            popup.classList.remove("show");
        }, 3000);
    }

    // Only target alerts within the messages container
    const alerts = document.querySelectorAll('.messages .alert');
    alerts.forEach(function(alert) {
        // Add transition for smooth fade out
        alert.style.transition = 'opacity 0.5s ease';
        
        // Set timeout to fade out and remove
        setTimeout(function() {
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.remove();
            }, 500);
        }, 3000);
    });
});
