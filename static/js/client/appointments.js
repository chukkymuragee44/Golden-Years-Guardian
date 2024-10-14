function addPrivateCareDetails() {
  connectToServer("client/caregiver", (caregiver) => {
    const caregiver_image = document.querySelector(
      ".caregiver .caregiver-image"
    );
    const caregiver_name = document.querySelector(".caregiver .caregiver-name");
    caregiver_image.style.backgroundImage = `url(${caregiver.image})`;
    caregiver_name.textContent = caregiver.name;
  });
}

function main() {
  connectToServer("client/caregiver/schedule", (schedule) => {
    appointment = schedule;
    const calendar_wrapper_details = document.querySelector(
      ".calendar-wrapper-details"
    );
    calendar_wrapper_details.append(render());
    addPrivateCareDetails();
  });
}
main();
