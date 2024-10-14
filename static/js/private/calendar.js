let open_event = {};
let today = new Date();
let appointment = {};

const months = [
  { month: "january", count: 31, days: otherMonthsDays() },
  {
    month: "february",
    count: 28,
    days: februaryDays(today.getFullYear()),
  },
  { month: "march", count: 31, days: otherMonthsDays() },
  { month: "april", count: 30, days: thirtyMonthsDays() },
  { month: "may", count: 31, days: otherMonthsDays() },
  { month: "june", count: 30, days: thirtyMonthsDays() },
  { month: "july", count: 31, days: otherMonthsDays() },
  { month: "august", count: 31, days: otherMonthsDays() },
  { month: "september", count: 30, days: thirtyMonthsDays() },
  { month: "october", count: 31, days: otherMonthsDays() },
  { month: "november", count: 30, days: thirtyMonthsDays() },
  { month: "december", count: 31, days: otherMonthsDays() },
];
const month_today = months[today.getMonth()].month;
const year_today = today.getFullYear();
const days_date = [
  "Sunday",
  "Monday",
  "Tuesay",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
];

function thirtyMonthsDays() {
  return [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
    22, 23, 24, 25, 26, 27, 28, 29, 30,
  ];
}

function otherMonthsDays() {
  return [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
    22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
  ];
}

function februaryDays(year) {
  return year % 4 === 0
    ? [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
        21, 22, 23, 24, 25, 26, 27, 28, 29,
      ]
    : [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
        21, 22, 23, 24, 25, 26, 27, 28,
      ];
}

function removeEventFromDatabase(date, event, index) {
  const year = today.getFullYear();
  const month = months[today.getMonth()].month;
  appointment[year][month][date].pop(index);
  connectToServer(
    `private/client/serving/schedule/remove/${event}/${year}/${month}/${date}`,
    () => {}
  );
}

function renderCalendarEvents(element, event, index, date) {
  const event_details = document.createElement("div");
  event_details.classList = "calendar-event-details";
  event_details.setAttribute("data-event", index);
  const event_details_text = document.createElement("div");
  event_details_text.textContent = event;
  event_details_text.setAttribute("data-event", index);
  const event_details_close = document.createElement("img");
  event_details_close.src = "../../../static/images/close.png";
  event_details_close.alt = "";
  event_details_close.setAttribute("data-event", index);
  event_details_close.addEventListener("click", ({ target }) => {
    const calendar_days = document.querySelectorAll(".calendar-day");
    calendar_days.forEach((day) => {
      const calendar_index = parseInt(day.dataset.calendar);
      if (calendar_index === date - 1) {
        const calendar_events = day.querySelectorAll(".calendar-event-details");
        calendar_events.forEach((calendar_event) => {
          const event_index = parseInt(calendar_event.dataset.event);
          const target_index = parseInt(target.dataset.event);
          if (event_index === target_index) {
            const event_element = calendar_event.querySelector(
              ".calendar-event-details div"
            );
            calendar_event.remove();
            removeEventFromDatabase(
              date,
              event_element.textContent,
              target_index
            );
          }
        });
      }
    });
  });
  event_details.append(event_details_text, event_details_close);
  element.append(event_details);
}

function careGiver(element) {
  const caregiver = document.createElement("div");
  caregiver.classList = "caregiver";
  const caregiver_image = document.createElement("div");
  caregiver_image.classList = "caregiver-image";
  caregiver_image.setAttribute(
    "style",
    "background-image: url(../../../static/images/avatar.png)"
  );
  const caregiver_details = document.createElement("div");
  caregiver_details.classList = "caregiver-details";
  const caregiver_name = document.createElement("div");
  caregiver_name.classList = "caregiver-name";
  caregiver_name.textContent = "";
  const caregiver_title = document.createElement("div");
  caregiver_title.classList = "caregiver-title";
  caregiver_title.textContent = "client";
  caregiver_details.append(caregiver_name, caregiver_title);
  caregiver.append(caregiver_image, caregiver_details);
  element.append(caregiver);
}

function removeCalendar() {
  const calendar = document.querySelector(".calendar-wrapper .calendar");
  if (calendar) {
    calendar.remove();
  }
}

function changeCalendarInputs(day, month, year) {
  const calendar_day = document.querySelector(".calendar-inputs .calendar-day");
  calendar_day.textContent = `${day},`;
  const calendar_month = document.querySelector(
    ".calendar-inputs .calendar-month"
  );
  calendar_month.textContent = month;
  const calendar_year = document.querySelector(
    ".calendar-inputs .calendar-year"
  );
  calendar_year.textContent = year;
}

function changeLeftCalendar() {
  const calendar_wrapper = document.querySelector(".calendar-wrapper");
  const previous_date = today.getDate();
  let previous_month = today.getMonth();
  let previous_year = today.getFullYear();
  previous_month--;
  if (previous_month < 0) {
    previous_year--;
    previous_month = 11;
  }
  const current_date = `${previous_year}-${
    previous_month + 1
  }-${previous_date}`;
  today = new Date(current_date);
  removeCalendar();
  calendar(calendar_wrapper, today.getMonth());
  changeCalendarInputs(
    days_date[today.getDay()],
    months[today.getMonth()].month,
    previous_year
  );
}

function changeRightCalendar() {
  const calendar_wrapper = document.querySelector(".calendar-wrapper");
  const previous_date = today.getDate();
  let previous_month = today.getMonth();
  let previous_year = today.getFullYear();
  previous_month++;
  if (previous_month > 11) {
    previous_year++;
    previous_month = 0;
  }
  const current_date = `${previous_year}-${
    previous_month + 1
  }-${previous_date}`;
  today = new Date(current_date);
  removeCalendar();
  calendar(calendar_wrapper, today.getMonth());
  changeCalendarInputs(
    days_date[today.getDay()],
    months[today.getMonth()].month,
    previous_year
  );
}

function calendarSliders(element) {
  const calendar_sliders = document.createElement("div");
  calendar_sliders.classList = "calendar-sliders";
  const calendar_left_slide = document.createElement("div");
  calendar_left_slide.classList = "calendar-left-slide";
  calendar_left_slide.addEventListener("click", changeLeftCalendar);
  const calendar_left_image = document.createElement("img");
  calendar_left_image.src = "../../../static/images/left-arrow.png";
  calendar_left_slide.append(calendar_left_image);
  const calendar_right_slide = document.createElement("div");
  calendar_right_slide.classList = "calendar-right-slide";
  calendar_right_slide.addEventListener("click", changeRightCalendar);
  const calendar_right_image = document.createElement("img");
  calendar_right_image.src = "../../../static/images/right-arrow.png";
  calendar_right_slide.append(calendar_right_image);
  calendar_sliders.append(calendar_left_slide, calendar_right_slide);
  element.append(calendar_sliders);
}

function calendarInputs(element, month_number) {
  const calendar_inputs = document.createElement("div");
  calendar_inputs.classList = "calendar-inputs";
  const calendar_day = document.createElement("div");
  calendar_day.classList = "calendar-day";
  calendar_day.textContent = `${days_date[today.getDay()]},`;
  const calendar_month = document.createElement("div");
  calendar_month.classList = "calendar-month";
  calendar_month.textContent = months[month_number].month;
  const calendar_year = document.createElement("div");
  calendar_year.classList = "calendar-year";
  calendar_year.textContent = today.getFullYear();
  calendar_inputs.append(calendar_day, calendar_month, calendar_year);
  element.append(calendar_inputs);
}

function calendarNav(element, month_number) {
  const calendar_nav = document.createElement("div");
  calendar_nav.classList = "calendar-nav";
  careGiver(calendar_nav);
  const calendar_today_container = document.createElement("div");
  calendar_today_container.classList = "calendar-today-container";
  const calendar_back = document.createElement("button");
  calendar_back.classList = "calendar-back";
  calendar_back.textContent = "Back";
  calendar_back.addEventListener("click", () => {
    location = "/private/appointments";
  });
  const calendar_today = document.createElement("button");
  calendar_today.classList = "calendar-today";
  calendar_today.textContent = "Today";
  calendar_today.addEventListener("click", () => {
    const calendar_wrapper = document.querySelector(".calendar-wrapper");
    today = new Date();
    removeCalendar();
    calendar(calendar_wrapper, today.getMonth());
    changeCalendarInputs(
      days_date[today.getDay()],
      months[today.getMonth()].month,
      today.getFullYear()
    );
  });
  calendar_today_container.append(calendar_back, calendar_today);
  calendar_nav.append(calendar_today_container);
  calendarSliders(calendar_nav);
  calendarInputs(calendar_nav, month_number);
  element.append(calendar_nav);
}

function showEventForm({ target }) {
  const days = document.querySelectorAll(".calendar-day");
  days.forEach((day) => {
    const day_index = parseInt(day.dataset.calendar);
    const target_index = parseInt(target.dataset.calendar);
    if (day_index === target_index) {
      const calendar_date = day.querySelector(".calendar-date");
      const calendar_month = document.querySelector(
        ".calendar-inputs .calendar-month"
      );
      const calendar_year = document.querySelector(
        ".calendar-inputs .calendar-year"
      );
      const date = calendar_date.textContent;
      const month = calendar_month.textContent;
      const year = calendar_year.textContent;
      open_event = { date, month, year };
      const event_date = document.getElementById("event-date");
      event_date.textContent = `${date} ${month} ${year}`;
      const event_form = document.querySelector(".calendar-event-form");
      event_form.style.display = "flex";
    }
  });
}

function calendarDay(element, date, index, active = false) {
  const calendar_day = document.createElement("div");
  calendar_day.classList = `calendar-day ${active ? "calendar-active" : ""}`;
  calendar_day.setAttribute("data-calendar", index);
  calendar_day.addEventListener("click", showEventForm);
  const calendar_date = document.createElement("div");
  calendar_date.classList = "calendar-date";
  calendar_date.textContent = date;
  calendar_date.setAttribute("data-calendar", index);
  const calendar_event = document.createElement("div");
  calendar_event.classList = "calendar-event";
  calendar_event.setAttribute("data-calendar", index);
  calendarEvent(calendar_event, date);
  calendar_day.append(calendar_date, calendar_event);
  element.append(calendar_day);
}

function calendar(element, month_number) {
  const calendar_wrapper = document.createElement("div");
  calendar_wrapper.classList = "calendar-wrapper";
  const calendar_element = document.createElement("div");
  calendar_element.classList = "calendar";
  const today_date = today.getDate();
  const days = months[month_number].days;
  days.forEach((day, index) => {
    if (day === today_date) {
      const month = months[today.getDay()].month;
      const year = today.getFullYear();
      calendarDay(
        calendar_element,
        day,
        index,
        month === month_today && year === year_today
      );
    } else {
      calendarDay(calendar_element, day, index);
    }
  });
  calendar_wrapper.append(calendar_element);
  element.append(calendar_wrapper);
}

function calendarEvent(element, day) {
  const year = today.getFullYear();
  const month = months[today.getMonth()].month;
  if (appointment[year]) {
    if (appointment[year][month]) {
      if (appointment[year][month][day]) {
        appointment[year][month][day].forEach((event, index) => {
          renderCalendarEvents(element, event, index, day);
        });
      }
    }
  }
}

function calendarContainer(element) {
  const calendar_container = document.createElement("div");
  calendar_container.classList = "calendar-container";
  const month_number = today.getMonth();
  calendarNav(calendar_container, month_number);
  calendar(calendar_container, month_number);
  element.append(calendar_container);
}

function render() {
  const content_wrapper = document.createElement("div");
  content_wrapper.classList = "content-wrapper";
  calendarContainer(content_wrapper);
  return content_wrapper;
}
