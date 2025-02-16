//js for add
document.addEventListener("DOMContentLoaded", function () {
    let ads = document.querySelectorAll(".ad-slide");
    let index = 0;

    function showNextAd() {
        ads.forEach((ad, i) => {
            ad.style.display = i === index ? "block" : "none";
        });
        index = (index + 1) % ads.length;
    }

//rotation
    showNextAd();
    setInterval(showNextAd, 10000); 
});
