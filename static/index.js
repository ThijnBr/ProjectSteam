document.addEventListener("DOMContentLoaded", function() {
  var userProfile = document.getElementsByClassName("user-profile")[0];
  var dropdownContent = document.getElementsByClassName("dropdown-content")[0];
  var arrow = document.getElementsByClassName("arrow")[0];

  // Adding event listener to userProfile to toggle the dropdown menu
  userProfile.addEventListener("click", function(event) {
    toggleMenu();
    event.stopPropagation(); // Prevents the click from propagating to the document
  });

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
});

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

function updateUserProfile() {
  const isLoggedIn = /* logic to check if user is logged in */ true;
  const userProfilePicture = document.getElementById('userProfilePicture');
  const username = document.getElementById('username');
  const loginLink = document.getElementById('loginLink');
  const signupLink = document.getElementById('signupLink');
  const viewAccountLink = document.getElementById('viewAccountLink');
  const signOutLink = document.getElementById('signOutLink');

  if (isLoggedIn) {
    // Update profile picture and username
    userProfilePicture.src = /* path to user's profile picture */ "path/to/profile-picture.jpg";
    username.textContent = /* user's name */ "John Doe";

    // Update dropdown menu
    loginLink.style.display = 'none';
    signupLink.style.display = 'none';
    viewAccountLink.style.display = 'block';
    signOutLink.style.display = 'block';
  } else {
    // Reset to default when not logged in
    userProfilePicture.src = "{{ url_for('static', filename='/resources/profile.jpg') }}";
    username.textContent = "";
  }
}


    