function submitForm() {
    const formData = new FormData(document.getElementById('signupForm'));
    fetch('/signup/', {
      method: 'POST',
      body: formData
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      window.location.href = '/signup/success/';
    })
    .catch(error => {
      console.error('There was a problem with your fetch operation:', error);
    });
  }
  
  document.getElementById('signupForm').addEventListener('submit', function(event) {
    event.preventDefault();
    submitForm();
  });
  let currentPage = 1;
  const form = document.getElementById('signupForm');
  const fieldsets = form.querySelectorAll('fieldset');
  
  function nextPage() {
    if (currentPage < fieldsets.length) {
      fieldsets[currentPage - 1].style.display = 'none';
      fieldsets[currentPage].style.display = 'block';
      currentPage++;
    }
  }
    