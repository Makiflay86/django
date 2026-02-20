let selectedFiles = [];
let mainFile = null;
const mainInput = document.querySelector('input[name="imagen"]');
const imageInput = document.getElementById('imageInput');
const previewContainer = document.getElementById('previewContainer');
const thumbContainer = document.getElementById('thumbContainer');
const carouselInner = document.getElementById('mainCarouselInner');
const formsetInputs = document.querySelectorAll('#hiddenFormset input[type="file"]');

mainInput.addEventListener('change', e => {
    mainFile = e.target.files[0];
    refreshVisuals();
});

imageInput.addEventListener('change', e => {
    const files = Array.from(e.target.files);
    files.forEach(file => {
        if (selectedFiles.length < formsetInputs.length) {
            selectedFiles.push(file);
            const div = document.createElement('div');
            div.className = 'new-preview-item';
            div.innerHTML = `<img src="${URL.createObjectURL(file)}" class="rounded border w-100 h-100" style="object-fit: cover;"><div class="remove-new"><i class="bi bi-trash"></i></div>`;
            div.querySelector('.remove-new').onclick = () => {
                selectedFiles = selectedFiles.filter(f => f !== file);
                div.remove();
                syncFormset();
                refreshVisuals();
            };
            previewContainer.appendChild(div);
        }
    });
    syncFormset();
    refreshVisuals();
});

function syncFormset() {
    formsetInputs.forEach((input, i) => {
        const dt = new DataTransfer();
        if (selectedFiles[i]) dt.items.add(selectedFiles[i]);
        input.files = dt.files;
    });
}

function refreshVisuals() {
    carouselInner.innerHTML = '';
    thumbContainer.innerHTML = '';
    let allImages = [];
    if (mainFile) allImages.push(mainFile);
    allImages = allImages.concat(selectedFiles);

    if (allImages.length === 0) {
        carouselInner.innerHTML = `<div class="carousel-item active"><div class="bg-light d-flex justify-content-center align-items-center" style="height: 380px;"><i class="bi bi-camera fs-1 text-secondary opacity-50"></i></div></div>`;
        return;
    }

    allImages.forEach((file, i) => {
        const url = URL.createObjectURL(file);
        const item = document.createElement('div');
        item.className = `carousel-item ${i === 0 ? 'active' : ''}`;
        item.innerHTML = `<img src="${url}" class="d-block w-100" style="height: 380px; object-fit: cover;">`;
        carouselInner.appendChild(item);

        const thumb = document.createElement('img');
        thumb.src = url;
        thumb.className = `thumb-selector ${i === 0 ? 'active' : ''}`;
        thumb.setAttribute('data-bs-target', '#carGallery');
        thumb.setAttribute('data-bs-slide-to', i);
        thumbContainer.appendChild(thumb);
    });
}

document.getElementById('carGallery').addEventListener('slid.bs.carousel', () => {
    document.querySelectorAll('.thumb-selector').forEach(el => el.classList.remove('active'));
    let activeIdx = Array.from(document.querySelectorAll('.carousel-item')).indexOf(document.querySelector('.carousel-item.active'));
    if (document.querySelector(`.thumb-selector[data-bs-slide-to="${activeIdx}"]`))
        document.querySelector(`.thumb-selector[data-bs-slide-to="${activeIdx}"]`).classList.add('active');
});