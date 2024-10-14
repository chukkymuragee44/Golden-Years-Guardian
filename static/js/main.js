let counter = 1;

function radioButtonSlides() {
  const radio1 = document.getElementById("slider-radio-1");
  const slide1 = document.getElementById("slide-1");
  radio1.addEventListener("change", (e) => {
    const radio_checked = e.target.checked;
    if (radio_checked) {
      slide1.style.marginLeft = "0";
      counter = 0;
    }
  });
  const radio2 = document.getElementById("slider-radio-2");
  radio2.addEventListener("change", (e) => {
    const radio_checked = e.target.checked;
    if (radio_checked) {
      slide1.style.marginLeft = "-100%";
      counter = 1;
    }
  });
  const radio3 = document.getElementById("slider-radio-3");
  radio3.addEventListener("change", (e) => {
    const radio_checked = e.target.checked;
    if (radio_checked) {
      slide1.style.marginLeft = "-200%";
      counter = 2;
    }
  });
  const radio4 = document.getElementById("slider-radio-4");
  radio4.addEventListener("change", (e) => {
    const radio_checked = e.target.checked;
    if (radio_checked) {
      slide1.style.marginLeft = "-300%";
      counter = 3;
    }
  });
  const radio5 = document.getElementById("slider-radio-5");
  radio5.addEventListener("change", (e) => {
    const radio_checked = e.target.checked;
    if (radio_checked) {
      slide1.style.marginLeft = "-400%";
      counter = 4;
    }
  });
}

function uncheckAllRadioButtons() {
  const radios = document.querySelectorAll(".slider-nav input");
  radios.forEach((radio) => {
    radio.checked = false;
  });
}

function autoSliderTransition() {
  const slide1 = document.getElementById("slide-1");

  setInterval(() => {
    uncheckAllRadioButtons();
    if (counter == 0) {
      const radio1 = document.getElementById("slider-radio-1");
      slide1.style.marginLeft = `0%`;
      radio1.checked = true;
    } else {
      const radio = document.getElementById(`slider-radio-${counter + 1}`);

      slide1.style.marginLeft = `-${counter}00%`;
      radio.checked = true;
    }
    counter++;
    if (counter == 5) {
      counter = 0;
    }
  }, 10000);
}

function main() {
  radioButtonSlides();
  autoSliderTransition();
}
main();
