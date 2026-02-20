"use strict";

var mainImgInput = document.querySelector('input[name="imagen"]');
var fileStatus = document.getElementById('file-status');
var btnRemoveMain = document.getElementById('btnRemoveMain');
var clearImgCheckbox = document.getElementById('imagen-clear_id');

if (mainImgInput) {
  mainImgInput.addEventListener('change', function (e) {
    if (this.files && this.files[0]) {
      var newImgUrl = URL.createObjectURL(this.files[0]);
      var mainItem = document.getElementById('mainItem');
      var thumbContainer = document.getElementById('thumbContainer');
      fileStatus.innerHTML = "<i class=\"bi bi-arrow-repeat\"></i> Nueva: ".concat(this.files[0].name);
      fileStatus.className = "small fw-bold text-primary";
      btnRemoveMain.style.display = "block";
      if (clearImgCheckbox) clearImgCheckbox.checked = false;
      mainItem.innerHTML = "<img src=\"".concat(newImgUrl, "\" class=\"d-block w-100\" id=\"mainImgPreview\" style=\"height: 380px; object-fit: cover;\">");
      var existingMainThumb = document.getElementById('mainThumb');

      if (existingMainThumb) {
        existingMainThumb.src = newImgUrl;
        existingMainThumb.style.display = "block";
      } else {
        var newThumb = document.createElement('img');
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
    fileStatus.innerHTML = "<i class=\"bi bi-x-circle-fill\"></i> Marcada para eliminar";
    fileStatus.className = "small fw-bold text-danger";
    document.getElementById('mainItem').innerHTML = "<div class=\"bg-light d-flex justify-content-center align-items-center\" style=\"height: 380px;\"><i class=\"bi bi-camera fs-1 text-secondary opacity-50\"></i></div>";
    if (document.getElementById('mainThumb')) document.getElementById('mainThumb').style.display = "none";
    this.style.display = "none";
  });
}

var selectedFiles = [];
var imageInput = document.getElementById('imageInput');
var previewContainer = document.getElementById('previewContainer');
imageInput.addEventListener('change', function (e) {
  var files = Array.from(e.target.files);
  files.forEach(function (file) {
    selectedFiles.push(file);
    var reader = new FileReader();

    reader.onload = function (event) {
      var div = document.createElement('div');
      div.className = 'new-preview-item';
      div.innerHTML = "<img src=\"".concat(event.target.result, "\" class=\"rounded border shadow-sm w-100 h-100\" style=\"object-fit: cover;\"><div class=\"remove-new\"><i class=\"bi bi-trash\"></i></div>");

      div.querySelector('.remove-new').onclick = function () {
        selectedFiles = selectedFiles.filter(function (f) {
          return f !== file;
        });
        div.remove();
        updateInputFiles();
      };

      previewContainer.appendChild(div);
    };

    reader.readAsDataURL(file);
  });
  updateInputFiles();
});

function updateInputFiles() {
  var dataTransfer = new DataTransfer();
  selectedFiles.forEach(function (file) {
    return dataTransfer.items.add(file);
  });
  imageInput.files = dataTransfer.files;
}

var carGallery = document.getElementById('carGallery');
carGallery.addEventListener('slid.bs.carousel', function () {
  document.querySelectorAll('.thumb-selector').forEach(function (el) {
    return el.classList.remove('active');
  });
  var activeIdx = Array.from(document.querySelectorAll('.carousel-item')).indexOf(document.querySelector('.carousel-item.active'));
  var targetThumb = document.querySelectorAll('.thumb-selector')[activeIdx];
  if (targetThumb) targetThumb.classList.add('active');
});
//# sourceMappingURL=cars_edit.dev.js.map
