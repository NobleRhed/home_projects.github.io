function showConfirmation() {
    const confirmation = document.getElementById('fileConfirmation');
    const file = document.getElementById('fileUpload').files[0];

    if (file) {
        confirmation.style.display = 'block';
    } else {
        confirmation.style.display = 'none';
    }
}
