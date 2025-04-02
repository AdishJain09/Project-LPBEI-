document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("loginForm").addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent default form submission

        // Get email and password values
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        // Dummy validation (Replace with backend authentication)
        const validEmail = "user@example.com";
        const validPassword = "password123";

        if (email === validEmail && password === validPassword) {
            localStorage.setItem("loggedIn", "true"); // Store login status
            window.location.href = "dashboard.html"; // Redirect to dashboard
        } else {
            alert("Invalid email or password! Please try again.");
        }
    });
});
