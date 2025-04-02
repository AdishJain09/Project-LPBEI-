// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get the login form
    const loginForm = document.querySelector('form');

    // Listen for the form submission
    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent default form submission

        // Get the form data
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        // Basic client-side validation (you can improve this)
        if (!email || !password) {
            alert('Please fill in both email and password!');
            return;
        }

        // Here, you would typically send the data to the server for validation (using fetch, XMLHttpRequest, etc.)
        // For now, just simulate a successful login:
        console.log('Logging in with:', email, password);
        
        // After a successful login, you could redirect the user to a new page (e.g., dashboard or home)
        // Replace the URL with your desired destination
        window.location.href = '/home';  // Redirect to home page (example)

    });
});

