"use strict";

function togglePassword(btn) {
  // Buscamos el input que está justo antes del botón dentro del input-group
  var input = btn.parentElement.querySelector('input');
  var icon = btn.querySelector('i');

  if (input.type === "password") {
    input.type = "text";
    icon.classList.replace('bi-eye-fill', 'bi-eye-slash-fill');
  } else {
    input.type = "password";
    icon.classList.replace('bi-eye-slash-fill', 'bi-eye-fill');
  }
}
//# sourceMappingURL=toggle_password.dev.js.map
