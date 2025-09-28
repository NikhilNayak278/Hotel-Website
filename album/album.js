const images = ['1.webp', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg', '7.jpeg'];
let currentIndex = 0;
const widthOfImage = 550;

const albumContainer = document.querySelector('.album-container');
const imgElement = document.getElementById('albumImage');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');

// Create all images once on page load
function initializeImages() {
    images.forEach((img, index) => {
        const image = new Image();
        image.src = `../images/${img}`;
        image.className = 'album-image';
        image.style.left = `${widthOfImage * (index - currentIndex)}px`;
        if(index === currentIndex) {
            image.style.transform = 'scale(1)';
            image.style.opacity = '1';
        } else {
            image.style.transform = 'scale(0.8)';
            image.style.opacity = '0.5';
        }
        albumContainer.appendChild(image);
    });
}

function nextImage() {
    currentIndex = (currentIndex + 1) % images.length;
    updateImages();
}

function prevImage() {
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    updateImages();
}

function updateImages() {
    const allImages = document.querySelectorAll('.album-image');
    allImages.forEach((image, index) => {
        // Update left position - this will now transition smoothly!
        image.style.left = `${widthOfImage * (index - currentIndex)}px`;
        
        if(index === currentIndex) {
            image.style.transform = 'scale(1)';
            image.style.opacity = '1';
        } else {
            image.style.transform = 'scale(0.8)';
            image.style.opacity = '0.5';
        }
    });
}
prevBtn.addEventListener('click', prevImage);
nextBtn.addEventListener('click', nextImage);

initializeImages();