document.addEventListener("DOMContentLoaded", function() {
    const minusBtn = document.querySelector(".minus");
    const plusBtn = document.querySelector(".plus");
    const quantityInput = document.getElementById("quantity-input");
    const hiddenQuantity = document.getElementById("hidden-quantity");

    minusBtn.addEventListener("click", function() {
        let currentValue = parseInt(quantityInput.value);
        if (currentValue > 1) {
            quantityInput.value = currentValue - 1;
            hiddenQuantity.value = quantityInput.value;
        }
    });

    plusBtn.addEventListener("click", function() {
        let currentValue = parseInt(quantityInput.value);
        quantityInput.value = currentValue + 1;
        hiddenQuantity.value = quantityInput.value;
    });

    quantityInput.addEventListener("input", function() {
        if (quantityInput.value < 1 || isNaN(quantityInput.value)) {
            quantityInput.value = 1;
        }
        hiddenQuantity.value = quantityInput.value;
    });
});