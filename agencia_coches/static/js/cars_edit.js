const mainImgInput = document.querySelector('input[name="imagen"]');
const fileStatus = document.getElementById('file-status');
const btnRemoveMain = document.getElementById('btnRemoveMain');
const clearImgCheckbox = document.getElementById('imagen-clear_id');

if (mainImgInput) {
    mainImgInput.addEventListener('change', function (e) {
        if (this.files && this.files[0]) {
            const newImgUrl = URL.createObjectURL(this.files[0]);
            const mainItem = document.getElementById('mainItem');
            const thumbContainer = document.getElementById('thumbContainer');

            fileStatus.innerHTML = `<i class="bi bi-arrow-repeat"></i> Nueva: ${this.files[0].name}`;
            fileStatus.className = "small fw-bold text-primary";
            btnRemoveMain.style.display = "block";
            if (clearImgCheckbox) clearImgCheckbox.checked = false;

            mainItem.innerHTML = `<img src="${newImgUrl}" class="d-block w-100" id="mainImgPreview" style="height: 380px; object-fit: cover;">`;

            let existingMainThumb = document.getElementById('mainThumb');
            if (existingMainThumb) {
                existingMainThumb.src = newImgUrl;
                existingMainThumb.style.display = "block";
            } else {
                const newThumb = document.createElement('img');
                newThumb.id = "mainThumb";
                newThumb.src = newImgUrl;
                newThumb.className = "rounded border shadow-sm thumb-selector active";
                newThumb.style = "width: 70px; height: 50px; object-fit: cover; cursor: pointer;";
                newThumb.setAttribute('data-bs-target', '#carGallery');
                newThumb.setAttribute('data-bs-slide-to', "0");
                thumbContainer.prepend(newThumb);
            }
        }
    });
}

if (btnRemoveMain) {
    btnRemoveMain.addEventListener('click', function () {
        mainImgInput.value = "";
        if (clearImgCheckbox) clearImgCheckbox.checked = true;
        fileStatus.innerHTML = `<i class="bi bi-x-circle-fill"></i> Marcada para eliminar`;
        fileStatus.className = "small fw-bold text-danger";
        document.getElementById('mainItem').innerHTML = `<div class="bg-light d-flex justify-content-center align-items-center" style="height: 380px;"><i class="bi bi-camera fs-1 text-secondary opacity-50"></i></div>`;
        if (document.getElementById('mainThumb')) document.getElementById('mainThumb').style.display = "none";
        this.style.display = "none";
    });
}

let selectedFiles = [];
const imageInput = document.getElementById('imageInput');
const previewContainer = document.getElementById('previewContainer');

imageInput.addEventListener('change', function (e) {
    const files = Array.from(e.target.files);
    files.forEach(file => {
        selectedFiles.push(file);
        const reader = new FileReader();
        reader.onload = function (event) {
            const div = document.createElement('div');
            div.className = 'new-preview-item';
            div.innerHTML = `<img src="${event.target.result}" class="rounded border shadow-sm w-100 h-100" style="object-fit: cover;"><div class="remove-new"><i class="bi bi-trash"></i></div>`;
            div.querySelector('.remove-new').onclick = function () {
                selectedFiles = selectedFiles.filter(f => f !== file);
                div.remove();
                updateInputFiles();
            };
            previewContainer.appendChild(div);
        }
        reader.readAsDataURL(file);
    });
    updateInputFiles();
});

function updateInputFiles() {
    const dataTransfer = new DataTransfer();
    selectedFiles.forEach(file => dataTransfer.items.add(file));
    imageInput.files = dataTransfer.files;
}

var carGallery = document.getElementById('carGallery');
carGallery.addEventListener('slid.bs.carousel', function () {
    document.querySelectorAll('.thumb-selector').forEach(el => el.classList.remove('active'));
    let activeIdx = Array.from(document.querySelectorAll('.carousel-item')).indexOf(document.querySelector('.carousel-item.active'));
    const targetThumb = document.querySelectorAll('.thumb-selector')[activeIdx];
    if (targetThumb) targetThumb.classList.add('active');
});