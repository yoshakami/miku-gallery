let offset = 0;
const limit = 20;
let isLoading = false;

function loadImages() {
    if (isLoading) return;
    isLoading = true;
    
    fetch(`/load_images?offset=${offset}&limit=${limit}`)
        .then(response => response.json())
        .then(data => {
            const imageGrid = document.getElementById('image-grid');
            
            if (data.length === 0) {
                window.onscroll = null;
                return;
            }
            
            data.forEach(image => {
                const img = document.createElement('img');
                img.src = "images/" + image.hash;
                img.alt = image.filename;
                img.loading = "lazy";
                img.classList.add('thumbnail');
                img.onclick = () => openModal(img.src, image.filename);  // Ajoute l'événement clic
                imageGrid.appendChild(img);
            });
            offset += limit;
            isLoading = false;
        })
        .catch(() => isLoading = false);
}
let isZoomed = false;

function openModal(src, captionText) {
    const modal = document.getElementById('image-modal');
    const modalImg = document.getElementById('modal-image');
    const caption = document.getElementById('caption');
    
    modal.style.display = "flex"; /* Use flex display for centering */
    modalImg.src = src;
    caption.innerText = captionText;
}

function closeModal() {
    const modal = document.getElementById('image-modal');
    modal.style.display = "none";
    isZoomed = false;  // Reset zoom state when closing modal
}

window.onload = () => {
    loadImages();
    
    window.onscroll = () => {
        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 100) {
            loadImages();
        }
    };

    // Close modal on click outside the image
    document.getElementById('image-modal').onclick = function (event) {
        if (event.target === this) {
            closeModal();
        }
    }
    // Close modal on click outside the image
    document.querySelectorAll('.modal-content')[0].onclick = function (event) {
        if (event.target === this) {
            closeModal();
        }
    }
};

// Make sure to remove any unnecessary calls to closeModal() directly in onload
