const form = document.getElementById('signupForm');
const sections = form.querySelectorAll('.form-section');
const prevButtons = form.querySelectorAll('.prevBtn');
const nextButtons = form.querySelectorAll('.nextBtn');
const submitBtn = document.querySelector('.submitBtn');
let currentStep = 0;

function showStep(stepIndex) {
    sections.forEach((section, index) => {
        if (index === stepIndex) {
            section.style.display = 'block';
        } else {
            section.style.display = 'none';
        }
    });

    // Show/hide buttons based on current step
    if (currentStep === 0) {
        prevButtons.forEach(button => {
            button.style.display = 'none';
        });
        nextButtons.forEach(button => {
            button.style.display = 'inline-block';
        });
        submitBtn.style.display = 'none';
    } else if (currentStep === sections.length - 1) {
        prevButtons.forEach(button => {
            button.style.display = 'inline-block';
        });
        nextButtons.forEach(button => {
            button.style.display = 'none';
        });
        submitBtn.style.display = 'inline-block';
    } else {
        prevButtons.forEach(button => {
            button.style.display = 'inline-block';
        });
        nextButtons.forEach(button => {
            button.style.display = 'inline-block';
        });
        submitBtn.style.display = 'none';
    }
}

function goToNextStep() {
    currentStep++;
    showStep(currentStep);
}

function goToPrevStep() {
    currentStep--;
    showStep(currentStep);
}

function handleSubmit(event) {
    event.preventDefault(); // Prevent default form submission

    // Collect form data
    const formData = new FormData(form);

    // Send form data to the server using fetch or XMLHttpRequest
    fetch(form.action, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            // Redirect or handle successful form submission
            window.location.href = '';
        } else {
            // Handle error response from the server
            console.error('Form submission failed:', response.statusText);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Add event listener for form submission
form.addEventListener('submit', handleSubmit);

// Add event listeners for previous and next buttons
prevButtons.forEach(button => {
    button.addEventListener('click', goToPrevStep);
});

nextButtons.forEach(button => {
    button.addEventListener('click', goToNextStep);
});

// Show initial step
showStep(currentStep);
