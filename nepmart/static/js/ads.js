let currentIndex = 0;
const images = document.querySelectorAll('.image-slide');
const imagesContainer = document.querySelector('.image-slider');

// Function to change images
function changeImage(direction) {
  currentIndex += direction;

  // Loop back to the start or end if at the boundaries
  if (currentIndex >= images.length) {
    currentIndex = 0;
  } else if (currentIndex < 0) {
    currentIndex = images.length - 1;
  }

  // Change the position of images container to show the next image
  imagesContainer.style.transform = `translateX(${-currentIndex * 100}%)`;

  // Reset the interval when the user manually changes the image
  clearInterval(interval);
  interval = setInterval(() => changeImage(1), 10000);
}

// Set interval to change images every 10 seconds
let interval = setInterval(() => changeImage(1), 10000);
