const toggleTheme = document.getElementById("toggleTheme");
const darkArrow = document.getElementById("dark-arrow");
const dropDown = document.getElementById("show-drop-down");
const editEvents = document.querySelectorAll(".edit__event");
const errorMsgs = document.querySelectorAll(".error__msg");
const dropDownList = document.querySelector(".inner__list");

// /////////Theme /////////
const applyTheme = (theme) => {
  document.body.classList.remove("light-mode", "dark-mode");
  document.body.classList.add(theme);

  // if (theme == "light-mode") {
  //   toggleTheme.setAttribute("src", "{% static 'images/dark-theme-icon.svg' %}");
  //   darkArrow.setAttribute("src", `images/arrow-down.svg`);
  // } else {
  //   toggleTheme.setAttribute("src", `images/light-theme-icon.svg`);
  //   darkArrow.setAttribute("src", `images/arrow-down-dk.svg`);
  // }
};

const savedTheme = localStorage.getItem("theme") || "dark-mode";
applyTheme(savedTheme);

toggleTheme.addEventListener("click", () => {
  const isLightMode = document.body.classList.contains("light-mode");

  const newTheme = isLightMode ? "dark-mode" : "light-mode";

  applyTheme(newTheme);
  localStorage.setItem("theme", newTheme);
});

// //////////////Handle Drop down ////////////
dropDown.addEventListener(
  "mouseover",
  () => (dropDownList.style.display = "block")
);
dropDownList.addEventListener(
  "mouseleave",
  () => (dropDownList.style.display = "none")
);
document.body.addEventListener("mousedown", (e) => {
  if (!dropDownList.contains(e.target)) {
    dropDownList.style.display = "none";
  }

  editEvents.forEach((editEvent) => {
    if (!editEvent.lastElementChild.contains(e.target)) {
      editEvent.lastElementChild.classList.remove("toggle");
    }
  });
});

editEvents.forEach((editEvent) => {
  editEvent.addEventListener("click", (e) => {
    editEvent.lastElementChild.classList.toggle("toggle");
  });
});



setTimeout(() => {
  errorMsgs.forEach(err => err.style.display = 'none') 
}, 2000)