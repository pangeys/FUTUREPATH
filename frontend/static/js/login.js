// Login form validation
const loginForm = document.getElementById("loginForm");

if (loginForm) {
    loginForm.addEventListener("submit", function(e) {
        e.preventDefault();

        let user = document.getElementById("username").value;
        let pass = document.getElementById("password").value;
        let msg = document.getElementById("message");

        // FIXED: Changed to correctPass instead of correct
        let correctUser = "admin";
        let correctPass = "1234";

        if(user === correctUser && pass === correctPass) {
            alert('Login successful!');
            // You can redirect to another page here if needed
            // window.location.href = '/dashboard';
        } else {
            // FIXED: Typo - "Incorect" → "Incorrect"
            alert('Incorrect username or password.');
            
            // Display message in the page if msg element exists
            if (msg) {
                msg.textContent = 'Incorrect username or password.';
                msg.style.color = 'red';
            }
        }
    });
}