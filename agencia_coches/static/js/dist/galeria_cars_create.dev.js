"use strict";

var multiUpload = document.getElementById('multi_upload');
var previewContainer = document.getElementById('preview-container');
var formsetInputs = document.querySelectorAll('input[name$="-imagen"]');
var occupiedIndices = new Array(10).fill(false);
multiUpload.addEventListener('change', function (e) {
  var files = Array.from(e.target.files);
  files.forEach(function (file) {
    var freeIndex = occupiedIndices.findIndex(function (status) {
      return status === false;
    });

    if (freeIndex !== -1 && freeIndex < 10) {
      occupiedIndices[freeIndex] = true;
      renderPreview(file, freeIndex);
      var dt = new DataTransfer();
      dt.items.add(file);
      formsetInputs[freeIndex].files = dt.files;
    }
  });
  this.value = "";
});

function renderPreview(file, index) {
  var reader = new FileReader();

  reader.onload = function (e) {
    var div = document.createElement('div');
    div.className = "col-6 col-md-4 col-lg-3 preview-item-".concat(index);
    div.innerHTML = "\n                <div class=\"preview-card position-relative\">\n                    <img src=\"".concat(e.target.result, "\" class=\"img-preview\">\n                    <button type=\"button\" onclick=\"removeFoto(").concat(index, ")\" \n                            class=\"btn-delete position-absolute top-0 end-0 m-1 shadow-sm\">\n                        &times;\n                    </button>\n                </div>\n            ");
    previewContainer.appendChild(div);
  };

  reader.readAsDataURL(file);
}

function removeFoto(index) {
  var element = document.querySelector(".preview-item-".concat(index));
  if (element) element.remove();
  formsetInputs[index].value = "";
  occupiedIndices[index] = false;
}
//# sourceMappingURL=galeria_cars_create.dev.js.map
