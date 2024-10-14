const image_file_extensions = [
  "image/jpg",
  "image/jpeg",
  "image/png",
  "image/gif",
];

function showProductImage(files) {
  const first_file = files[0];
  const first_file_extension = first_file.type;
  const profile_image = document.querySelector(".content-details .profile-image");
  const profile_image_placeholder = document.getElementById("profile-image-placeholder")
  console.log(profile_image.style.backgroundImage)
  if (image_file_extensions.includes(first_file_extension)) {
    const reader = new FileReader();
    reader.onload = () => {
      const result = reader.result;
      profile_image.style.backgroundImage = `url(${result})`;
      profile_image_placeholder.value = result;
    };
    reader.readAsDataURL(first_file);
  } else {
    alert("invalid file type");
  }
}

function loadProfileImage() {
  const profile_edit = document.querySelector(".profile-edit");
  const profile_file = document.getElementById("profile-file");
  profile_edit.addEventListener("click", () => profile_file.click());
  profile_file.addEventListener("change", (e) => {
    showProductImage(e.target.files);
  });
}

function main() {
  loadProfileImage();
}
main();
