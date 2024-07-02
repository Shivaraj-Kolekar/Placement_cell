// login.js

function clearErrors() {
    const errors = document.getElementsByClassName('formerror');
    for (let item of errors) {
        item.innerHTML = "";
    }
}

function seterror(id, error) {
    const element = document.getElementById(id);
    element.innerHTML = error;
}

function validateLogin() {
    let returnval = true;
    clearErrors();
    
    // Email validation
    const email = document.forms['login-form']["email"].value;
    if (!/^\d{8}@pvgcoet.ac.in$/.test(email)) {
        seterror("email_error", "*Email must contain 8 digits followed by @pvgcoet.ac.in");
        returnval = false;
    }
    return returnval;
}

function togglePasswordVisibility(element) {
    var passwordField = element.previousElementSibling;
    var visibilityIcon = element.querySelector("i");

    if (passwordField.type === "password") {
        passwordField.type = "text";
        visibilityIcon.classList.remove("fa-eye");
        visibilityIcon.classList.add("fa-eye-slash");
    } else {
        passwordField.type = "password";
        visibilityIcon.classList.remove("fa-eye-slash");
        visibilityIcon.classList.add("fa-eye");
    }
}
