document.getElementById("loginForm").addEventListener("submit", function(e) {
    e.preventDefault(); // prevent refresh

    let user = document.getElementById("username").value;
    let pass = document.getElementById("password").value;
    let msg = document.getElementById("message");

    let correctUser = "admin";
    let correctPass = "1234";

    if (user === correctUser && pass === correctPass) {
        msg.style.color = "green";
        msg.textContent = "Login successful!";
        // window.location.href = "dashboard.html";
    } else {
        msg.style.color = "red";
        msg.textContent = "Invalid username or password.";
    }
});