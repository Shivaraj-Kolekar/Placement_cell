
let currentStep = 1;
const form = document.getElementById('signup-form');
const steps = form.getElementsByClassName('step');

function showStep(stepNumber) {
  for (let i = 0; i < steps.length; i++) {
    steps[i].style.display = (i + 1 === stepNumber) ? 'block' : 'none';
  }
}

function nextStep() {
  if (currentStep < steps.length) {
    currentStep++;
    showStep(currentStep);
  }
}

function prevStep() {
  if (currentStep > 1) {
    currentStep--;
    showStep(currentStep);
  }
}

showStep(currentStep);
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


// Function to toggle password visibility
function togglePasswordVisibility(inputId) {
    var input = document.getElementById(inputId);
    var icon = document.querySelector('#' + inputId + ' + .toggle-password i');

    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

// Example usage: Toggle password visibility
document.querySelectorAll('.toggle-password').forEach(function (element) {
    element.addEventListener('click', function () {
        var inputId = this.previousElementSibling.id;
        togglePasswordVisibility(inputId);
    });
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
    // Company name validation (only if placement status is "Placed")
    const placementStatus = document.getElementById("placement_status").value;
    if (placementStatus === "Placed") {
        const company_name = document.forms['signup-form']['company_name'].value;
        if (company_name.length < 5) {
            seterror("company_name_error", "*Company name should be at least 5 characters long");
            returnval = false;
        } else if (company_name.length > 50) {
            seterror("company_name_error", "*Company name should not be greater than 50 characters long");
            returnval = false;
        }
        
        // Salary validation
        const salaryField = document.forms['signup-form']['salary'];
        if (salaryField.value.trim() === "") {
            seterror("salary_error", "*Please enter a salary");
            returnval = false;
        } else {
            const salary = parseFloat(salaryField.value);
            if (isNaN(salary) || salary < 0) {
                seterror("salary_error", "*Salary should be a valid number and not negative");
                returnval = false;
            }
        }
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

 function validatestdUpdate()
 {
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
    // Company name validation (only if placement status is "Placed")
    const placementStatus = document.getElementById("placement_status").value;
    if (placementStatus === "Placed") {
        const company_name = document.forms['signup-form']['company_name'].value;
        if (company_name.length < 5) {
            seterror("company_name_error", "*Company name should be at least 5 characters long");
            returnval = false;
        } else if (company_name.length > 50) {
            seterror("company_name_error", "*Company name should not be greater than 50 characters long");
            returnval = false;
        }
        
        // Salary validation
        const salaryField = document.forms['signup-form']['salary'];
        if (salaryField.value.trim() === "") {
            seterror("salary_error", "*Please enter a salary");
            returnval = false;
        } else {
            const salary = parseFloat(salaryField.value);
            if (isNaN(salary) || salary < 0) {
                seterror("salary_error", "*Salary should be a valid number and not negative");
                returnval = false;
            }
        }
    }
    return returnval;

 }




function jobValidation() {
  clearErrors();
  let returnval = true;

  // Step 1: Job Role Information Validation
  const job_id = document.getElementById('job_id').value;
  const job_title = document.getElementById('job_title').value;
  const company_name = document.getElementById('company_name').value;
  const location = document.getElementById('location').value;
  const salary = document.getElementById('salary').value;

  if (job_id.length < 3) {
    seterror("job_id_error", "*Job Id should be at least 3 characters long");
    returnval = false;
  }
  if (parseInt(job_id) < 0) {
    seterror("job_id_error", "*Job Id should not be negative");
    returnval = false;
  }

  if (job_title.length < 5) {
    seterror("job_title_error", "*Job Title should be at least 5 characters long");
    returnval = false;
  } else if (job_title.length > 50) {
    seterror("job_title_error", "*Job Title should not be greater than 50 characters long");
    returnval = false;
  }

  if (company_name.length < 5) {
    seterror("company_name_error", "*Company name should be at least 5 characters long");
    returnval = false;
  } else if (company_name.length > 50) {
    seterror("company_name_error", "*Company name should not be greater than 50 characters long");
    returnval = false;
  }

  if (location.length < 3) {
    seterror("location_error", "*Location should be at least 3 characters long");
    returnval = false;
  } else if (location.length > 50) {
    seterror("location_error", "*Location should not be greater than 50 characters long");
    returnval = false;
  }

  if (salary.length === 0) {
    seterror("salary_error", "*Salary is required");
    returnval = false;
  }

  // Step 2: Academic Details Validation
  const required_CGPA = document.getElementById('required_CGPA').value;
  const required_marks = document.getElementById('required_marks').value;
  const required_branchs = document.querySelectorAll('input[name="required_branchs"]:checked');

  if (required_CGPA.length === 0) {
    seterror("required_CGPA_error", "*Required CGPA is required");
    returnval = false;
  } else if (isNaN(required_CGPA) || required_CGPA < 0 || required_CGPA > 10) {
    seterror("required_CGPA_error", "*Required CGPA should be a number between 0 and 10");
    returnval = false;
  }

  if (required_marks.length === 0) {
    seterror("required_marks_error", "*Required Percentages is required");
    returnval = false;
  } else if (isNaN(required_marks) || required_marks < 0 || required_marks > 100) {
    seterror("required_marks_error", "*Required Percentages should be a number between 0 and 100");
    returnval = false;
  }

  if (required_branchs.length === 0) {
    seterror("required_branchs_error", "*At least one branch should be selected");
    returnval = false;
  }
  
  // Step 3: Exam Details Validation
  const date_last = document.getElementById('date_last').value;
  const date_exam = document.getElementById('date_exam').value;
  const venue = document.getElementById('venue').value;

  const last_date = new Date(date_last);
  const exam_date = new Date(date_exam);
  const currentDate = new Date();

  if (last_date <= currentDate) {
    seterror("date_last_error", "*Last Date should be in the future");
    returnval = false;
  }

  if (exam_date <= currentDate) {
    seterror("date_exam_error", "*Exam Date should be in the future");
    returnval = false;
  }

  if (venue.length < 5) {
    seterror("venue_error", "*Venue should be at least 5 characters long");
    returnval = false;
  } else if (venue.length > 50) {
    seterror("venue_error", "*Venue should not be greater than 50 characters long");
    returnval = false;
  }

  return returnval;
}


function setSystemTime() {
  const systemTimeInput = document.getElementById('system_time');
  systemTimeInput.value = new Date().toISOString();
}


/* function validateLogin() {
  let returnval = true;
  clearErrors();
  
  // Email validation
  const email = document.forms['login-form']["email"].value;
  if (!/^\d{8}@pvgcoet.ac.in$/.test(email)) {
      seterror("email_error", "*Email must contain 8 digits followed by @pvgcoet.ac.in");
      returnval = false;
  }
  return returnval;
} */