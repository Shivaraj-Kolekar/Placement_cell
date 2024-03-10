function showDateTimePicker(inputId) {
    var datetimePicker = document.getElementById('datetimePicker' + inputId);
    if (datetimePicker.style.display === 'none') {
        datetimePicker.style.display = 'block';
    } else {
        datetimePicker.style.display = 'none';
    }
}
