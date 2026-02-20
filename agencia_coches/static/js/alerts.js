// Auto-cerrar las alertas tras 4 segundos
setTimeout(function () {
    let toasts = document.querySelectorAll('.toast');
    toasts.forEach(t => t.classList.remove('show'));
}, 4000);