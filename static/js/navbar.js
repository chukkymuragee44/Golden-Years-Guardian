function closeProfile() {
  const items = document.querySelector(".profile-items");
  if (items.style.display === "block") {
    items.style.display = "none";
  }
}

function toggleProfile() {
  const profile = document.querySelector(".profile-image");
  if (profile) {
    profile.addEventListener("click", () => {
      closeNotifications();
      const items = document.querySelector(".profile-items");
      if (items.style.display === "none") {
        items.style.display = "block";
      } else {
        items.style.display = "none";
      }
    });
  }
}

function closeNotifications() {
  const content = document.querySelector(
    ".notifications .notification-content"
  );
  if (content.style.display === "block") {
    content.style.display = "none";
  }
}

function toggleNotifications() {
  const bell = document.querySelector(".notifications .notification-nav");
  if (bell) {
    bell.addEventListener("click", () => {
      closeProfile();
      const content = document.querySelector(
        ".notifications .notification-content"
      );
      if (content.style.display === "none") {
        content.style.display = "block";
      } else {
        content.style.display = "none";
      }
    });
  }
}

function main() {
  toggleNotifications();
  toggleProfile();
}
main();
