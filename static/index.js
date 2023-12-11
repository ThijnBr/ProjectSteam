var userProfile = document.getElementsByClassName("user-profile")[0];
var dropdownContent = document.getElementsByClassName("dropdown-content")[0];
var arrow = document.getElementsByClassName("arrow")[0];

function toggleMenu() {
  dropdownContent.classList.toggle("show");
  arrow.classList.toggle("rotate");
}


function closeMenu(event) {
  if (!userProfile.contains(event.target)) {
    dropdownContent.classList.remove("show");
    arrow.classList.remove("rotate");
  }
}

document.addEventListener("click", closeMenu);

const formatter = new Intl.DateTimeFormat("en-GB", { 
  weekday: "long", 
  month: "long", 
  day: "numeric", 
  hour: "2-digit", 
  minute: "2-digit", 
});

function showTime() {
  var date = new Date(); 
  var formattedDate = formatter.format(date); 
  document.getElementById("clock").innerHTML = formattedDate; 
}

window.onload = function() {
  showTime(); 
  setInterval(showTime, 1000); 
}
