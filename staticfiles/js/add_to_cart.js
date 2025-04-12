document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("add-to-cart-form");
    if (!form) return; // Exit if form doesn't exist

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        // Check if user is authenticated (this will be set in the template)
        const isAuthenticated = form.hasAttribute('data-authenticated');
        if (!isAuthenticated) {
            window.location.href = '/login/?next=' + window.location.pathname;
            return;
        }

        const formData = new FormData(form);
        const actionURL = form.getAttribute("data-url");

        fetch(actionURL, {
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
            },
            credentials: 'same-origin'
        })
            .then(response => {
                if (response.status === 403) {
                    // User is not authenticated
                    window.location.href = '/login/?next=' + window.location.pathname;
                    throw new Error('Not authenticated');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    showCartAlert("Item added to the cart! 🛒", "success");
                } else {
                    if (data.redirect) {
                        window.location.href = data.redirect;
                    } else {
                        showCartAlert(data.message || "Failed to add item to cart!", "error");
                    }
                }
            })
            .catch(error => {
                if (error.message === 'Not authenticated') {
                    return; // Already handled above
                }
                showCartAlert("Please log in to add items to cart", "error");
            });
    });

    function showCartAlert(message, type) {
        let alertBox = document.createElement("div");
        alertBox.textContent = message;

        // Common styles
        const commonStyles = {
            position: "fixed",
            top: "-50px",
            left: "50%",
            transform: "translateX(-50%)",
            color: "white",
            padding: "15px 25px",
            borderRadius: "8px",
            textAlign: "center",
            fontSize: "16px",
            fontWeight: "bold",
            boxShadow: "0 4px 10px rgba(0, 0, 0, 0.2)",
            zIndex: "1000",
            opacity: "0",
            transition: "top 0.5s ease-out, opacity 0.5s"
        };

        // Type-specific styles
        const typeStyles = {
            success: {
                backgroundColor: "#4CAF50"
            },
            error: {
                backgroundColor: "#FF5722"
            }
        };

        // Apply styles
        Object.assign(alertBox.style, commonStyles, typeStyles[type] || typeStyles.error);

        document.body.appendChild(alertBox);

        // Show alert
        setTimeout(() => {
            alertBox.style.top = "20px";
            alertBox.style.opacity = "1";
        }, 100);

        // Hide alert
        setTimeout(() => {
            alertBox.style.top = "-50px";
            alertBox.style.opacity = "0";
            setTimeout(() => alertBox.remove(), 500);
        }, 3000);
    }
});
