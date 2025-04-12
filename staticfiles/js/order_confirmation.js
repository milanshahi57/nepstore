document.addEventListener('DOMContentLoaded', function() {
    const successMessage = document.querySelector('.confirmation-header');
    if (successMessage) {
        // Add transition property to the element
        successMessage.style.transition = 'all 0.5s ease';
        
        setTimeout(function() {
            // Fade out and slide up
            successMessage.style.opacity = '0';
            successMessage.style.transform = 'translateY(-20px)';
            
            // Remove the element after animation completes
            setTimeout(function() {
                successMessage.remove();
            }, 500);
        }, 3000);
    }
}); 