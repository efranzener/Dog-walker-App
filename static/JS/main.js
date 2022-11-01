
const rmCheck = document.getElementById("rememberMe");
let emailInput = document.getElementById("email-login");

if (localStorage.checkbox && localStorage.checkbox !== " ") {
  rmCheck.setAttribute("checked", "checked");
  emailInput.value = localStorage.email;
} else {
  rmCheck.removeAttribute("checked");
  emailInput.checked = " ";
}

function lsRememberMe() {
  if (rmCheck.checked && emailInput.value !== " ") {
    localStorage.email = emailInput.value;
    localStorage.checkbox = rmCheck.value;
  } else {
    localStorage.email = " ";
    localStorage.checkbox = " ";
  }
}


function myFunction() {
    var showPassword = document.getElementById("password-login");
    if (showPassword.type === "password") {
    showPassword.type = "text";
    } else {
    showPassword.type = "password";
    }
  }


  document.getElementById("profiledog").onchange = function () {
    let src = URL.createObjectURL(this.files[0]);
    document.getElementById("dog-pic").src = src;
}