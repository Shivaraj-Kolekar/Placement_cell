let currentStep = 1;
const form = document.getElementById('signup-form');
const steps = form.getElementsByClassName('step');

function showStep(stepNumber) {
  for (let i = 0; i < steps.length; i++) {
    if (i + 1 === stepNumber) {
      steps[i].style.display = 'block';
    } else {
      steps[i].style.display = 'none';
    }
  }
}

function nextStep(stepNumber) {
  if (stepNumber === currentStep && currentStep < steps.length) {
    currentStep++;
    showStep(currentStep);
  }
}

function prevStep(stepNumber) {
  if (stepNumber === currentStep && currentStep > 1) {
    currentStep--;
    showStep(currentStep);
  }
}

showStep(currentStep);

function toggleFields() {
  var placementStatus = document.getElementById("placement_status").value;
  var additionalFields = document.getElementById("additionalFields");
  if (placementStatus === "Placed") {
    additionalFields.classList.remove("hidden");
  } else {
    additionalFields.classList.add("hidden");
  }
}
var currentTime = new Date();

// Format the time as per your requirement
var formattedTime = currentTime.toISOString(); // Or any other format you prefer

// Set the value of the hidden field to the formatted time
document.getElementById("system_time").value = formattedTime; // Corrected ID to "system_time"


