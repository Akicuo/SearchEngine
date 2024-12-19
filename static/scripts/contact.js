document.getElementById('contact-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    // Get form values
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;

    // Simple validation
    if (name && email && message) {
        // Simulate a successful submission
        document.getElementById('response-message').innerText = 'Message sent successfully!';
        document.getElementById('contact-form').reset(); // Reset the form
    } else {
        document.getElementById('response-message').innerText = 'Please fill in all fields.';
    }
});
