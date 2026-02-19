const multiUpload = document.getElementById('multi_upload');
const previewContainer = document.getElementById('preview-container');
const formsetInputs = document.querySelectorAll('input[name$="-imagen"]');
let occupiedIndices = new Array(10).fill(false);

multiUpload.addEventListener('change', function (e) {
    const files = Array.from(e.target.files);
    files.forEach(file => {
        const freeIndex = occupiedIndices.findIndex(status => status === false);
        if (freeIndex !== -1 && freeIndex < 10) {
            occupiedIndices[freeIndex] = true;
            renderPreview(file, freeIndex);
            const dt = new DataTransfer();
            dt.items.add(file);
            formsetInputs[freeIndex].files = dt.files;
        }
    });
    this.value = "";
});

function renderPreview(file, index) {
    const reader = new FileReader();
    reader.onload = function (e) {
        const div = document.createElement('div');
        div.className = `col-6 col-md-4 col-lg-3 preview-item-${index}`;
        div.innerHTML = `
                <div class="preview-card position-relative">
                    <img src="${e.target.result}" class="img-preview">
                    <button type="button" onclick="removeFoto(${index})" 
                            class="btn-delete position-absolute top-0 end-0 m-1 shadow-sm">
                        &times;
                    </button>
                </div>
            `;
        previewContainer.appendChild(div);
    }
    reader.readAsDataURL(file);
}

function removeFoto(index) {
    const element = document.querySelector(`.preview-item-${index}`);
    if (element) element.remove();
    formsetInputs[index].value = "";
    occupiedIndices[index] = false;
}