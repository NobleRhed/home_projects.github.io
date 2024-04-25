function showConfirmation() {
    const confirmation = document.getElementById('fileConfirmation');
    const file = document.getElementById('fileUpload').files[0];

    if (file) {
        confirmation.style.display = 'block';
    } else {
        confirmation.style.display = 'none';
    }
}

function dropHandler(ev) {
    ev.preventDefault();

    if (ev.dataTransfer.items) {
        // Use DataTransferItemList interface to access the file(s)
        for (var i = 0; i < ev.dataTransfer.items.length; i++) {
            // If dropped items aren't files, reject them
            if (ev.dataTransfer.items[i].kind === 'file') {
                var file = ev.dataTransfer.items[i].getAsFile();
                document.getElementById('fileUpload').files = ev.dataTransfer.files;
                showConfirmation();
                break; // Assuming you only want one file, break after getting the first
            }
        }
    }

    removeDragData(ev);
}

function dragOverHandler(ev) {
    ev.preventDefault();
}

function showConfirmation() {
    const confirmation = document.getElementById('fileConfirmation');
    const file = document.getElementById('fileUpload').files[0];
    const preview = document.getElementById('preview');

    if (file) {
        confirmation.style.display = 'block';
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                preview.innerHTML = '<img src="' + e.target.result + '" style="max-width: 100%; max-height: 300px;" />';
            };
            reader.readAsDataURL(file);
        } else {
            preview.innerHTML = `<p>${file.name}</p>`;
        }
    } else {
        confirmation.style.display = 'none';
    }
}

function removeDragData(ev) {
    if (ev.dataTransfer.items) {
        // Use DataTransferItemList interface to remove the drag data
        ev.dataTransfer.items.clear();
    } else {
        // Use DataTransfer interface to remove the drag data
        ev.dataTransfer.clearData();
    }
}
