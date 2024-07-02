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

// Multi-step form validation and navigation functions
let currentStep = 1;
const form = document.getElementById('signup-form');
const steps = form.getElementsByClassName('step');

function showStep(stepNumber) {
  for (let i = 0; i < steps.length; i++) {
    steps[i].style.display = (i + 1 === stepNumber) ? 'block' : 'none';
  }
}

function nextStep(stepNumber) {
  if (validateStep(stepNumber)) {
    if (currentStep < steps.length) {
      currentStep++;
      showStep(currentStep);
    }
  }
}

function prevStep() {
  if (currentStep > 1) {
    currentStep--;
    showStep(currentStep);
  }
}

showStep(currentStep);

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

function validateStep(stepNumber) {
  let isValid = true;
  clearErrors();

  if (stepNumber === 1) {
    // Name validation
    const name = document.forms['signup-form']["name"].value;
    const hasDigit = /\d/.test(name);
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(name);
    if (name.length < 5 || hasDigit || hasSpecialChar) {
      seterror("name_error", "*Name is too short or contains a digit/special character");
      isValid = false;
    }

    // CRN number validation
    const crn_number = document.forms['signup-form']["crn_number"].value;
    if (!/^\d{8}$/.test(crn_number)) {
      seterror("crn_number_error", "*CRN number must be exactly 8 digits");
      isValid = false;
    }

    // Phone number validation
    const phone = document.forms['signup-form']["mobile_number"].value;
    if (phone.length != 10) {
      seterror("mobile_number_error", "*Phone number should be of 10 digits");
      isValid = false;
    }
  } else if (stepNumber === 2) {
    // CGPA validation
    const cgpa = parseFloat(document.forms['signup-form']['CGPA'].value);
    if (isNaN(cgpa) || cgpa < 0 || cgpa > 10) {
      seterror("cgpa_error", "*CGPA should be between 0 and 10");
      isValid = false;
    }

    // Aggregate marks validation
    const aggregateMarks = parseFloat(document.forms['signup-form']['aggregate_marks'].value);
    if (isNaN(aggregateMarks) || aggregateMarks < 0 || aggregateMarks > 100) {
      seterror("aggregate_marks_error", "*Aggregate marks should be between 0 and 100");
      isValid = false;
    }

    // 10th marks validation
    const marks10th = parseFloat(document.forms['signup-form']['mark_10th'].value);
    if (isNaN(marks10th) || marks10th < 0 || marks10th > 100) {
      seterror("mark_10th_error", "*10th marks should be between 0 and 100");
      isValid = false;
    }
  } else if (stepNumber === 3) {
    // Company name validation
    const company_name = document.forms['signup-form']['company_name'].value;
    if (company_name) {
      if (company_name.length < 5) {
        seterror("company_name_error", "*Company name should be at least 5 characters long");
        isValid = false;
      } else if (company_name.length > 50) {
        seterror("company_name_error", "*Company name should not be greater than 50 characters long");
        isValid = false;
      }
    }

    // Salary validation
    const salary = parseFloat(document.forms['signup-form']['salary'].value);
    if (salary) {
      if (isNaN(salary) || salary < 0) {
        seterror("salary_error", "*Salary should not be negative");
        isValid = false;
      }
    }
  } else if (stepNumber === 4) {
    // Email validation
    const email = document.forms['signup-form']["email"].value;
    if (!/\S+@\S+\.\S+/.test(email)) {
      seterror("email_error", "*Please enter a valid email address");
      isValid = false;
    }

    // Password validation
    const password = document.getElementById('password').value;
    const retypePassword = document.getElementById('retype-password').value;
    if (password !== retypePassword) {
      document.getElementById('password-error').style.display = 'block';
      isValid = false;
    } else {
      document.getElementById('password-error').style.display = 'none';
    }
  }

  return isValid;
}

function toggleFields() {
  var placementStatus = document.getElementById("placement_status").value;
  var additionalFields = document.getElementById("additionalFields");
  additionalFields.classList.toggle("hidden", placementStatus !== "Placed");
}

document.getElementById('mark_12th').addEventListener('change', function () {
  toggleDiplomaMarks();
  validateMarks();
});

document.getElementById('diploma_marks').addEventListener('change', function () {
  toggle12thMarks();
  validateMarks();
});

function toggleDiplomaMarks() {
  const mark12th = document.getElementById('mark_12th').value;
  const diplomaMarks = document.getElementById('diploma_marks');

  if (mark12th) {
    diplomaMarks.disabled = true;
    diplomaMarks.value = '';
  } else {
    diplomaMarks.disabled = false;
  }
}

function toggle12thMarks() {
  const diplomaMarks = document.getElementById('diploma_marks').value;
  const mark12th = document.getElementById('mark_12th');

  if (diplomaMarks) {
    mark12th.disabled = true;
    mark12th.value = '';
  } else {
    mark12th.disabled = false;
  }
}

function validateMarks() {
  const mark12th = document.getElementById('mark_12th').value;
  const diplomaMarks = document.getElementById('diploma_marks').value;

  document.getElementById('12th_marks_error').innerText = '';
  document.getElementById('diploma_marks_error').innerText = '';

  if (mark12th && diplomaMarks) {
    document.getElementById('12th_marks_error').innerText = 'Please enter only one of 12th Marks or Diploma Marks.';
    document.getElementById('diploma_marks_error').innerText = 'Please enter only one of 12th Marks or Diploma Marks.';
  }
}

document.getElementById('signup-form').addEventListener('submit', function (event) {
  if (!validateForm()) {
    event.preventDefault();
  }
});



function validateForm() {
  let returnval = true;
  clearErrors();

  // Name validation
  const name = document.forms['signup-form']["name"].value;
  const hasDigit = /\d/.test(name); // Check if name contains a digit
  const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(name);
  if (name.length < 5 || hasDigit || hasSpecialChar) {
    seterror("name_error", "*Name is too short or contains a digit/special character");
    returnval = false;
  }

  // CRN number validation
  const crn_number = document.forms['signup-form']["crn_number"].value;
  if (!/^\d{8}$/.test(crn_number)) {
    seterror("crn_number_error", "*CRN number must be exactly 8 digits");
    returnval = false;
  }

  // Phone number validation
  const phone = document.forms['signup-form']["mobile_number"].value;
  if (phone.length != 10) {
    seterror("mobile_number_error", "*Phone number should be of 10 digits");
    returnval = false;
  }

  // CGPA validation
  const cgpa = parseFloat(document.forms['signup-form']['CGPA'].value);
  if (isNaN(cgpa) || cgpa < 0 || cgpa > 10) {
    seterror("cgpa_error", "*CGPA should be between 0 and 10");
    returnval = false;
  }

  // Aggregate marks validation
  const aggregateMarks = parseFloat(document.forms['signup-form']['aggregate_marks'].value);
  if (isNaN(aggregateMarks) || aggregateMarks < 0 || aggregateMarks > 100) {
    seterror("aggregate_marks_error", "*Aggregate marks should be between 0 and 100");
    returnval = false;
  }

  // 10th marks validation
  const marks10th = parseFloat(document.forms['signup-form']['mark_10th'].value);
  if (isNaN(marks10th) || marks10th < 0 || marks10th > 100) {
    seterror("mark_10th_error", "*10th marks should be between 0 and 100");
    returnval = false;
  }

  // Validate only one of 12th marks or Diploma marks
  const mark12th = document.getElementById('mark_12th').value;
  const diplomaMarks = document.getElementById('diploma_marks').value;
  if (mark12th && diplomaMarks) {
    seterror('12th_marks_error', 'Please enter only one of 12th Marks or Diploma Marks.');
    seterror('diploma_marks_error', 'Please enter only one of 12th Marks or Diploma Marks.');
    returnval = false;
  }

  // Company name validation
  const company_name = document.forms['signup-form']['company_name'].value;
  if (company_name) {
    if (company_name.length < 5) {
      seterror("company_name_error", "*Company name should be at least 5 characters long");
      returnval = false;
    } else if (company_name.length > 50) {
      seterror("company_name_error", "*Company name should not be greater than 50 characters long");
      returnval = false;
    }
  }

  // Salary validation
  const salary = parseFloat(document.forms['signup-form']['salary'].value);
  if (salary) {
    if (isNaN(salary) || salary < 0) {
      seterror("salary_error", "*Salary should not be negative");
      returnval = false;
    }
  }

  // Email validation
  const email = document.forms['signup-form']["email"].value;
  if (!/^\d{8}@pvgcoet.ac.in$/.test(email)) {
    seterror("email_error", "*Email must contain 8 digits followed by @pvgcoet.ac.in");
    returnval = false;
  }

  // Password validation
  const password = document.getElementById('password').value;
  const retypePassword = document.getElementById('retype-password').value;
  if (password !== retypePassword) {
    document.getElementById('password-error').style.display = 'block';
    returnval = false;
  } else {
    document.getElementById('password-error').style.display = 'none';
  }

  return returnval;
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


