let selectedFile = null;

const dropArea = document.getElementById("drop-area");
const fileInput = document.getElementById("fileElem");

// Drag events
dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropArea.style.background = "#e3f2fd";
});

dropArea.addEventListener("dragleave", () => {
    dropArea.style.background = "white";
});

dropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    selectedFile = e.dataTransfer.files[0];
    dropArea.innerHTML = selectedFile.name;
});

// Click to select
dropArea.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", () => {
    selectedFile = fileInput.files[0];
    dropArea.innerHTML = selectedFile.name;
});

function uploadPDF() {
    if (!selectedFile) {
        alert("Select a PDF first!");
        return;
    }

    let formData = new FormData();
    formData.append("pdf", selectedFile);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        console.log(data);  // debug

        document.getElementById("preview-section").style.display = "block";

        // preview load
        document.getElementById("pdf-preview").src = data.preview_url;

        // download link
        document.getElementById("download-btn").href = data.download_url;
    })
    .catch(err => {
        console.error(err);
        alert("Error uploading PDF");
    });
}




// file name show
fileInput.addEventListener("change", () => {
    selectedFile = fileInput.files[0];
    document.getElementById("file-name").innerText = "Selected: " + selectedFile.name;
});

// loader
function uploadPDF() {
    if (!selectedFile) {
        alert("Select a PDF first!");
        return;
    }

    document.getElementById("loader").style.display = "block";

    let formData = new FormData();
    formData.append("pdf", selectedFile);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("loader").style.display = "none";
        document.getElementById("preview-section").style.display = "block";
        document.getElementById("pdf-preview").src = data.preview_url;
        document.getElementById("download-btn").href = data.download_url;
    });
}