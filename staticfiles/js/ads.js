document.addEventListener("DOMContentLoaded", function () {
  let currentIndex = 0;
  const images = document.querySelectorAll(".image-slide");
  const imagesContainer = document.querySelector(".image-slider");

  if (images.length === 0 || !imagesContainer) return;

  function showImage(index) {
      images.forEach((img, i) => {
          img.style.opacity = i === index ? "1" : "0"; // Use opacity instead of display
          img.style.transition = "opacity 0.5s ease-in-out"; // Smooth transition
      });
  }

  function changeImage(direction) {
      currentIndex += direction;

      if (currentIndex >= images.length) {
          currentIndex = 0; // Loop back to the first image
      } else if (currentIndex < 0) {
          currentIndex = images.length - 1; // Loop to the last image
      }

      showImage(currentIndex);

      // Reset the interval when manually changing the image
      clearInterval(interval);
      interval = setInterval(() => changeImage(1), 10000);
  }

  // Show the first image initially
  showImage(currentIndex);

  // Auto-change images every 10 seconds
  let interval = setInterval(() => changeImage(1), 10000);

  // Attach event listeners to buttons
  document.querySelector(".prev").addEventListener("click", () => changeImage(-1));
  document.querySelector(".next").addEventListener("click", () => changeImage(1));
});
