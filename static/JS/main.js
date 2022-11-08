"use strict"


let rmCheck = document.getElementById("rememberMe");
let emailInput = document.getElementById("email-login");

if (localStorage.checkbox && localStorage.checkbox !== "") {
  rmCheck.setAttribute("checked", "checked");
  emailInput.value = localStorage.email;
} else {
  rmCheck.removeAttribute("checked");
  emailInput.checked = "";
}

function lsRememberMe() {
  if (rmCheck.checked && emailInput.value !== "") {
    localStorage.email = emailInput.value;
    localStorage.checkbox = rmCheck.value;
  } else {
    localStorage.email = "";
    localStorage.checkbox = "";
  }
}


function myFunction() {
  let showLoginPassword = document.getElementById("password-login");
  if (showLoginPassword.type === "password") {
  showLoginPassword.type = "text";
  } else {
  showLoginPassword.type = "password";
  }
}


function showNewPassword() {
  const showNewPassword = document.getElementById("newpassword");
  if (showNewPassword.type === "password") {
  showNewPassword.type = "text";
  } else {
  showNewPassword.type = "password";
  };
}

function showConfPwd() {
  const showNewConfirmPassword = document.getElementById("new_confirmpassword");
  if (showNewConfirmPassword.type == "password") {
  showNewConfirmPassword.type = "text";
  } else {
  showNewConfirmPassword.type = "password";
  };
  }



// document.getElementById("profilepic").onchange = function () {
//   let src = URL.createObjectURL(this.files[0]);
//   document.getElementById("prof-pic").src = src;
// }


document.getElementById("start-date").addEventListener('change', (evt) => {
  evt.preventDefault();
  console.log("hello")
  const formData = {
    selectedDate: date = document.getElementById('start-date').value,
    selectedSitter: sitterId = document.getElementById('#sitter_id').value,
  };
  const queryString = new URLSearchParams(formData).toString();
  // you could also hard code url to '/status?order=123'
  const url = `/create_booking?${queryString}`;

  fetch(url)
    .then((response) => response.text())
    .then((times_list) => {
      document.getElementById('start_time').value = times_list;
      console.log(times_list);
      console.log("hello");
  });
});


// ###############


// document.querySelector('#start-date').addEventListener('change', (evt) => {
//   evt.preventDefault();

//   // Get user input from a form
//   const formData = {
//     sitterid: sitterId = document.querySelector('#sitter_id').value,
//     date: document.querySelector('#start-date').value,
//   };

//   // construct query string – will be in the format of 'city=CITY_VAL&address=ADDRESS_VAL'
//   const queryString = new URLSearchParams(formData).toString();

//   fetch(`/create_booking?${queryString}`)
//     .then((response) => response.json())
//     .then((responseJson) => {
//       // Display response from the server
//       document.querySelector('#start-time').innerText = responseJson;
//       console.log(responseJson)

//     });
// });