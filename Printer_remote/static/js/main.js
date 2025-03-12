
/**
 * BEWARE: Doop
 * show confirmation of file upload. Ensure the preview is displayed for files sent in. Works with drag and drop.
 */
function showConfirmation() {
    const confirmation = document.getElementById('fileConfirmation');
    const file = document.getElementById('fileUpload').files[0];

    if (file) {
        confirmation.style.display = 'block';
    } else {
        confirmation.style.display = 'none';
    }
}

/**
 * 
 * handles the drag and drop of files. This 
 */
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

/**
 * 
 * prevents the browser from just opening a file dragged into the window. 
 */
function dragOverHandler(ev) {
    ev.preventDefault();
}

/** 
 * BEWARE: Doop.
 *  this showConfirmation might be better. compare and contrast their outputs. Here we handle if the file is an image (display in preview box) or not (display file name).
 */

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

/**
 * 
 * Function to remove the drag data. This is called after the file has been processed.
 */
function removeDragData(ev) {
    if (ev.dataTransfer.items) {
        // Use DataTransferItemList interface to remove the drag data
        ev.dataTransfer.items.clear();
    } else {
        // Use DataTransfer interface to remove the drag data
        ev.dataTransfer.clearData();
    }
}

// TODO: Handle failed print requests

// TODO: Return message if print fails - use newly practiced async with Promises and await

