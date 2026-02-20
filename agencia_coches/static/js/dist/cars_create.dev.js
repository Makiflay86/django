"use strict";

var selectedFiles = [];
var mainFile = null;
var mainInput = document.querySelector('input[name="imagen"]');
var imageInput = document.getElementById('imageInput');
var previewContainer = document.getElementById('previewContainer');
var thumbContainer = document.getElementById('thumbContainer');
var carouselInner = document.getElementById('mainCarouselInner');
var formsetInputs = document.querySelectorAll('#hiddenFormset input[type="file"]');
mainInput.addEventListener('change', function (e) {
  mainFile = e.target.files[0];
  refreshVisuals();
});
imageInput.addEventListener('change', function (e) {
  var files = Array.from(e.target.files);
  files.forEach(function (file) {
    if (selectedFiles.length < formsetInputs.length) {
      selectedFiles.push(file);
      var div = document.createElement('div');
      div.className = 'new-preview-item';
      div.innerHTML = "<img src=\"".concat(URL.createObjectURL(file), "\" class=\"rounded border w-100 h-100\" style=\"object-fit: cover;\"><div class=\"remove-new\"><i class=\"bi bi-trash\"></i></div>");

      div.querySelector('.remove-new').onclick = function () {
        selectedFiles = selectedFiles.filter(function (f) {
          return f !== file;
        });
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
  formsetInputs.forEach(function (input, i) {
    var dt = new DataTransfer();
    if (selectedFiles[i]) dt.items.add(selectedFiles[i]);
    input.files = dt.files;
  });
}

function refreshVisuals() {
  carouselInner.innerHTML = '';
  thumbContainer.innerHTML = '';
  var allImages = [];
  if (mainFile) allImages.push(mainFile);
  allImages = allImages.concat(selectedFiles);

  if (allImages.length === 0) {
    carouselInner.innerHTML = "<div class=\"carousel-item active\"><div class=\"bg-light d-flex justify-content-center align-items-center\" style=\"height: 380px;\"><i class=\"bi bi-camera fs-1 text-secondary opacity-50\"></i></div></div>";
    return;
  }

  allImages.forEach(function (file, i) {
    var url = URL.createObjectURL(file);
    var item = document.createElement('div');
    item.className = "carousel-item ".concat(i === 0 ? 'active' : '');
    item.innerHTML = "<img src=\"".concat(url, "\" class=\"d-block w-100\" style=\"height: 380px; object-fit: cover;\">");
    carouselInner.appendChild(item);
    var thumb = document.createElement('img');
    thumb.src = url;
    thumb.className = "thumb-selector ".concat(i === 0 ? 'active' : '');
    thumb.setAttribute('data-bs-target', '#carGallery');
    thumb.setAttribute('data-bs-slide-to', i);
    thumbContainer.appendChild(thumb);
  });
}

document.getElementById('carGallery').addEventListener('slid.bs.carousel', function () {
  document.querySelectorAll('.thumb-selector').forEach(function (el) {
    return el.classList.remove('active');
  });
  var activeIdx = Array.from(document.querySelectorAll('.carousel-item')).indexOf(document.querySelector('.carousel-item.active'));
  if (document.querySelector(".thumb-selector[data-bs-slide-to=\"".concat(activeIdx, "\"]"))) document.querySelector(".thumb-selector[data-bs-slide-to=\"".concat(activeIdx, "\"]")).classList.add('active');
});
//# sourceMappingURL=cars_create.dev.js.map
