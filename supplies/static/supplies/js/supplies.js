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

  // when the delete is confirmed then call delete_car_image url
  document
    .getElementById("confirmDelete")
    .addEventListener("click", function () {
      if (!selectedImageId) return;
      loaderToggel(false);

      fetch(`/supply/image/${selectedImageId}/delete/`, {
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
            showToast(`Couldn't delete the image, ${res.statusText}`);
            throw new Error(`HTTP error ${res.status}`);
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
            // show success message
            showToast("Image deleted successfully!", "text-bg-success");
          } else {
            showToast("Error deleting image", "text-bg-danger");
          }
        })
        .catch((error) => {
          showToast("Error deleting image", "text-bg-danger");
          console.error("Error:", error);
        })
        .finally(() => {
          loaderToggel(true);
        });
    });

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
      col.className = "col-12 col-md-4 position-relative";

      col.innerHTML = `
              <div class="border shadow-sm overflow-hidden position-relative">
                  <img src="${e.target.result}" class="img-fluid rounded" alt="preview">
                  <button type="button" value="&times;" class="btn btn-sm btn-danger delete-btn">delete</button>
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

  // show message as a bootstrap toast
  function showToast(message, bgColorClass) {
    const toastEl = document.getElementById('message-toast');

    // Get the current scroll position and viewport size
    const scrollTop = window.scrollY;
    const viewportHeight = window.innerHeight;
    const toastHeight = toastEl.offsetHeight;

    // Position: center of the visible viewport
    toastEl.style.top = `${scrollTop + (viewportHeight - toastHeight) / 2}px`;
    toastEl.style.right = `5%`;
    
    // Add bg color class
    toastEl.classList.forEach(cls => {
      if (cls.startsWith("text-bg-")) {
        toastEl.classList.remove(cls);
      }
    });
    toastEl.classList.add(bgColorClass);

    // Display the message
    const content = document.querySelector(
      "#message-toast .toast-body"
    );
    content.innerText = message;
    const btoast = bootstrap.Toast.getOrCreateInstance(
      toastEl, { delay: 4500 }
    );
    btoast.show();
    setTimeout(() => btoast.hide(), 5000);
  }

  //close the confirmation modal
  function closeModal() {
    const modal = bootstrap.Modal.getInstance(
      document.getElementById("confirm-modal")
    );
    modal.hide();
  }

  // loader show/hide
  function loaderToggel(hide) {
    const loader = document.getElementById("loader");
    const modal = document.getElementById("confirm-modal");
    loader.style.visibility = hide ? "hidden" : "visible";
    modal.style.zIndex = hide ? "1100" : "10";
  }
});