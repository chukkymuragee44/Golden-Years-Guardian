const content_table = document.querySelector(".content-table");
const client_details = document.querySelector(".client-details");

function hideDetails() {
  const back = document.querySelector(".client-actions .back button");
  back.addEventListener("click", () => {
    client_details.style.display = "none";
    content_table.style.display = "grid";
  });
}

function showDetails(element) {
  client_details.style.display = "grid";
}

function showClientDetails() {
  const more_details = document.querySelector(".actions .more button");
  more_details.addEventListener("click", ({ target }) => {
    const table_ids = document.querySelectorAll(".table-id");
    const target_dataset = parseInt(target.dataset.client);
    table_ids.forEach((element) => {
      const dataset = parseInt(element.dataset.client);
      if (dataset === target_dataset) {
        content_table.style.display = "none";
        showDetails(element);
      }
    });
  });
}

function main() {
  showClientDetails();
  hideDetails();
}
main();
