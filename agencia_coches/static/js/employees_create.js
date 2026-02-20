document.addEventListener('DOMContentLoaded', function () {
    // Inicializar Popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    popoverTriggerList.map(function (el) { return new bootstrap.Popover(el) });

    const form = document.getElementById('employeeForm');
    const passInput = document.getElementById('id_password');
    const passError = document.getElementById('password-error');

    // Validación de contraseña en el Submit
    form.addEventListener('submit', function (e) {
        const pass = passInput ? passInput.value : "";
        const isValid = pass.length >= 8 && /[A-Z]/.test(pass) && /[0-9]/.test(pass);
        if (!isValid && passInput) {
            e.preventDefault();
            passError.classList.remove('d-none');
            passInput.focus();
        }
    });

    // Live Preview de Texto
    form.addEventListener('input', function () {
        const user = form.querySelector('[name="username"]')?.value || "";
        const ape = form.querySelector('[name="apellidos"]')?.value || "";
        const pto = form.querySelector('[name="puesto"]')?.value || "Puesto / Cargo";
        document.getElementById('previewFullName').innerText = (user + " " + ape).trim() || "Nuevo Empleado";
        document.getElementById('previewRole').innerText = pto;
    });

    // Live Preview de Foto
    const photoInput = document.querySelector('input[name="foto"]');
    if (photoInput) {
        photoInput.addEventListener('change', function () {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = e => {
                    document.getElementById('profilePreview').src = e.target.result;
                    document.getElementById('btnRemovePhoto').style.display = "inline-block";
                };
                reader.readAsDataURL(this.files[0]);
            }
        });
    }

    document.getElementById('btnRemovePhoto').addEventListener('click', function () {
        if (photoInput) photoInput.value = "";
        document.getElementById('profilePreview').src = "https://cdn-icons-png.flaticon.com/512/149/149071.png";
        this.style.display = "none";
    });
});