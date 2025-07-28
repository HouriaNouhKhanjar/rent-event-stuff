/**
 * upload images in supply create/edit form
 * */
document.addEventListener("DOMContentLoaded", function () {
  // selectedImageId determines the id of image to be deleted
  var selectedImageId;
  document.querySelectorAll(".delete-image-btn").forEach((btn) => {
    btn.addEventListener("click", function () {
      selectedImageId = this.dataset.imageId;
    });
});

 var confirmDelete =  document.getElementById("confirm-delete");

 if(confirmDelete) {
    confirmDelete.addEventListener("click", function () {
      if (!selectedImageId) return;
      loaderToggel(false);

      fetch(`/supplies/image/${selectedImageId}/delete/`, {
        method: "DELETE",
        headers: {
          "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
            .value,
          "X-Requested-With": "XMLHttpRequest"
        }
      })
        .then((res) => {
          if (!res.ok) {
            closeModal();
            window.location.reload();
          }
          return res.json();
        })
        .then((data) => {
          if (data.success) {
            // remove image preview
            document
              .getElementById(`image-preview-${selectedImageId}`)
              .remove(false);
            closeModal();
            window.location.reload();
          } else {
            window.location.reload();
          }
        })
        .catch((error) => {
          window.location.reload();
          console.error("Error:", error);
        })
        .finally(() => {
          loaderToggel(true);
        });
    });
 }
  /**
   * remove duplicate image input
   * */
  var element = document.getElementById("div_id_images");
  if (element) {
    element.remove();
  }

  //drag and drop images in car forms
  const dropArea = document.getElementById("drop-area");
  const input = document.getElementById("id-supply-image");
  const preview = document.getElementById("preview");

  document.querySelector(".upload-image-btn").addEventListener("click", function () {
       document.getElementById('id-supply-image').click();
  });

  // Virtual file list
  let fileBuffer = new DataTransfer();

  // Drag & Drop
  dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropArea.classList.add("bg-light");
  });

  dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("bg-light");
  });

  // every time changes the images list
  // preview the change on html
  dropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    dropArea.classList.remove("bg-light");
    handleFiles(e.dataTransfer.files);
  });

  input.addEventListener("change", () => {
    handleFiles(input.files);
  });

  function handleFiles(files) {
    for (let file of files) {
      addFileToPreview(file);
      fileBuffer.items.add(file);
    }
    input.files = fileBuffer.files;
  }

  function addFileToPreview(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      const col = document.createElement("div");
      col.className = "col-12 col-md-4 mt-2 mt-md-0 position-relative";

      col.innerHTML = `
              <div class="border shadow-sm overflow-hidden position-relative">
                  <img src="${e.target.result}" class="img-fluid rounded" alt="preview">
                  <button type="button" value="&times;" class="btn btn-sm btn-danger delete-btn w-100 mt-2">delete</button>
              </div>
          `;
      preview.appendChild(col);

      const deleteBtn = col.querySelector(".delete-btn");
      deleteBtn.addEventListener("click", () => {
        removeFile(file);
        col.remove();
      });
    };
    reader.readAsDataURL(file);
  }

  /**
   * remove image from file buffer
   */
  function removeFile(fileToRemove) {
    let newBuffer = new DataTransfer();
    for (let i = 0; i < fileBuffer.items.length; i++) {
      const file = fileBuffer.items[i].getAsFile();
      if (file !== fileToRemove) {
        newBuffer.items.add(file);
      }
    }
    fileBuffer = newBuffer;
    input.files = fileBuffer.files;
  }

  //close the confirmation modal
  function closeModal() {
    $("#confirm-modal").modal('hide');
  }

  // loader show/hide
  function loaderToggel(hide) {
    const loader = document.getElementById("loader");
    const modal = document.getElementById("confirm-modal");
    loader.style.visibility = hide ? "hidden" : "visible";
    modal.style.zIndex = hide ? "1100" : "10";
  }
});