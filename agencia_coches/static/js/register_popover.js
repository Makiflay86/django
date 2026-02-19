// Inicializar todos los popovers de Bootstrap
document.addEventListener('DOMContentLoaded', function () {
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    });

    // Aplicar clases de Bootstrap a los inputs que vienen de Django automáticamente
    const inputs = document.querySelectorAll('#registerForm input, #registerForm select');
    inputs.forEach(input => {
        input.classList.add('form-control');
    });
});