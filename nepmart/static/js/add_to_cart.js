document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("add-to-cart-form");

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // ❌ Prevent default form submission (no redirect)

        const formData = new FormData(form);
        const actionURL = form.getAttribute("data-url"); // ✅ Get URL from form

        fetch(actionURL, {
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest", // ✅ Important for Django
            },
        })
        .then(response => response.json()) // ✅ Expect JSON response
        .then(data => {
            if (data.success) {
                showCartAlert(); // Show custom styled alert when the item is added successfully
            } else {
                showErrorAlert(); // Show error alert in case of failure
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
    });

    // Function to show the "Item added to the cart" alert
    function showCartAlert() {
        let alertBox = document.createElement("div");
        alertBox.textContent = "Item added to the cart! 🛒";
        
        // Styling
        alertBox.style.position = "fixed";
        alertBox.style.top = "-50px"; // Start position (hidden)
        alertBox.style.left = "50%";
        alertBox.style.transform = "translateX(-50%)";
        alertBox.style.backgroundColor = "#4CAF50"; // Green success color
        alertBox.style.color = "white";
        alertBox.style.padding = "15px 25px";
        alertBox.style.borderRadius = "8px";
        alertBox.style.textAlign = "center";
        alertBox.style.fontSize = "16px";
        alertBox.style.fontWeight = "bold";
        alertBox.style.boxShadow = "0 4px 10px rgba(0, 0, 0, 0.2)";
        alertBox.style.zIndex = "1000";
        alertBox.style.opacity = "0";
        alertBox.style.transition = "top 0.5s ease-out, opacity 0.5s";

        document.body.appendChild(alertBox);

        // Show alert (Slide down)
        setTimeout(() => {
            alertBox.style.top = "20px";
            alertBox.style.opacity = "1";
        }, 100);

        // Hide alert after 3 seconds
        setTimeout(() => {
            alertBox.style.top = "-50px";
            alertBox.style.opacity = "0";
            setTimeout(() => alertBox.remove(), 500);
        }, 3000);
    }

    // Function to show the error alert (if any)
    function showErrorAlert() {
        let alertBox = document.createElement("div");
        alertBox.textContent = "Failed to add item to cart! Please try again.";

        // Styling for error alert
        alertBox.style.position = "fixed";
        alertBox.style.top = "-50px"; // Start position (hidden)
        alertBox.style.left = "50%";
        alertBox.style.transform = "translateX(-50%)";
        alertBox.style.backgroundColor = "#FF5722"; // Red failure color
        alertBox.style.color = "white";
        alertBox.style.padding = "15px 25px";
        alertBox.style.borderRadius = "8px";
        alertBox.style.textAlign = "center";
        alertBox.style.fontSize = "16px";
        alertBox.style.fontWeight = "bold";
        alertBox.style.boxShadow = "0 4px 10px rgba(0, 0, 0, 0.2)";
        alertBox.style.zIndex = "1000";
        alertBox.style.opacity = "0";
        alertBox.style.transition = "top 0.5s ease-out, opacity 0.5s";

        document.body.appendChild(alertBox);

        // Show alert (Slide down)
        setTimeout(() => {
            alertBox.style.top = "20px";
            alertBox.style.opacity = "1";
        }, 100);

        // Hide alert after 3 seconds
        setTimeout(() => {
            alertBox.style.top = "-50px";
            alertBox.style.opacity = "0";
            setTimeout(() => alertBox.remove(), 500);
        }, 3000);
    }
});
