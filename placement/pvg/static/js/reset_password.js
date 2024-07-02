// Function to validate passwords
function resetvalidatePasswords() {
    const password1 = document.getElementById('password1').value;
    const password2 = document.getElementById('password2').value;
    let isValid = true;

    // Clear previous error messages
    document.getElementById('password1-error').textContent = '';
    document.getElementById('password2-error').textContent = '';

    // Validate password match
    if (password1 !== password2) {
        document.getElementById('password2-error').textContent = 'The two password fields didn’t match.';
        isValid = false;
    }

    // Validate password length
    if (password1.length < 8) {
        document.getElementById('password1-error').textContent = 'This password is too short. It must contain at least 8 characters.';
        isValid = false;
    }

    // Validate password complexity
    const commonPasswords = ['12345678', 'password', '123456789', '1234567', '12345', '1234567890'];
    if (commonPasswords.includes(password1)) {
        document.getElementById('password1-error').textContent += ' This password is too common.';
        isValid = false;
    }

    // Validate password is not entirely numeric
    if (!isNaN(password1)) {
        document.getElementById('password1-error').textContent += ' This password is entirely numeric.';
        isValid = false;
    }

    return isValid;
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
