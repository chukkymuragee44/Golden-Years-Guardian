function saveEvent(event) {
  let add = false;
  if (!appointment[open_event.year]) {
    add = true;
    appointment[open_event.year] = {};
  }
  if (!appointment[open_event.year][open_event.month]) {
    appointment[open_event.year][open_event.month] = {};
  }
  if (!appointment[open_event.year][open_event.month][open_event.date]) {
    appointment[open_event.year][open_event.month][open_event.date] = [];
  }
  appointment[open_event.year][open_event.month][open_event.date].push(event);
  if (add) {
    saveCalenderEventToDatabase();
  } else {
    updateCalenderEventToDatabase(event);
  }
}

function updateCalenderEventToDatabase(event) {
  connectAndSendDataToServer(
    `private/client/serving/schedule/${open_event.year}/${open_event.month}/${open_event.date}`,
    { event },
    () => {}
  );
}

function saveCalenderEventToDatabase() {
  connectAndSendDataToServer(
    "private/client/serving/schedule",
    appointment,
    () => {}
  );
}

function clearExistingEvents(element) {
  const events = element.querySelectorAll(".calendar-event-details");
  events.forEach((event) => {
    event.remove();
  });
}

function addCalendarEventToDOM(element) {
  if (appointment[open_event.year][open_event.month][open_event.date]) {
    appointment[open_event.year][open_event.month][open_event.date].forEach(
      (event, index) => {
        renderCalendarEvents(element, event, index, open_event.date);
      }
    );
  }
}

function addCalendarEvent() {
  const event_form = document.querySelector(".calendar-event-form form");
  event_form.addEventListener("submit", (e) => {
    e.preventDefault();
    const event = e.target.event.value;
    if (event === "") {
      alert("please enter an event");
    } else {
      const days = document.querySelectorAll(".calendar .calendar-day");
      days.forEach((day) => {
        const date_number = parseInt(day.dataset.calendar);
        if (date_number === open_event.date - 1) {
          const calendar_event = day.querySelector(".calendar-event");
          clearExistingEvents(calendar_event);
          saveEvent(event);
          addCalendarEventToDOM(calendar_event);
          const event_form = document.querySelector(".calendar-event-form");
          event_form.style.display = "none";
          e.target.event.value = "";
        }
      });
    }
  });
}

function clientDetails() {
  connectToServer("private/client/serving", (client) => {
    const caregiver_image = document.querySelector(
      ".caregiver .caregiver-image"
    );
    const caregiver_name = document.querySelector(".caregiver .caregiver-name");
    caregiver_image.style.backgroundImage = `url(${client.photo})`;
    caregiver_name.textContent = `${client.first_name} ${client.last_name}`;
  });
}

function closeEventForm() {
  const event_form = document.querySelector(".calendar-event-form");
  const event_close = document.querySelector(
    ".calendar-event-form .close-event img"
  );
  event_close.addEventListener("click", () => {
    event_form.style.display = "none";
  });
}

function main() {
  connectToServer("private/client/serving/schedule", (schedule) => {
    appointment = schedule;
    const calendar_wrapper_details = document.querySelector(
      ".calendar-wrapper-details"
    );
    calendar_wrapper_details.append(render());
    addCalendarEvent();
    clientDetails();
    closeEventForm();
  });
}
main();
