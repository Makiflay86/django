document.getElementById('confirmDelete').addEventListener('click', function () {
    document.getElementById('foto-clear_id').checked = true;
    document.getElementById('profilePreview').src = "https://cdn-icons-png.flaticon.com/512/149/149071.png";
    bootstrap.Modal.getInstance(document.getElementById('deletePhotoModal')).hide();
});