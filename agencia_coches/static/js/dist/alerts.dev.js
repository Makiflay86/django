"use strict";

// Auto-cerrar las alertas tras 4 segundos
setTimeout(function () {
  var toasts = document.querySelectorAll('.toast');
  toasts.forEach(function (t) {
    return t.classList.remove('show');
  });
}, 4000);
//# sourceMappingURL=alerts.dev.js.map
