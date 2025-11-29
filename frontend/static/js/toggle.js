// Password visibility toggle functionality
const input = document.getElementById('password');
const toggle = document.getElementById('togglePassword');

// Check if elements exist before adding event listener
if (input && toggle) {
    toggle.addEventListener('click', () => {
        const isPassword = input.type === 'password';
        input.type = isPassword ? 'text' : 'password';
        toggle.className = isPassword ? 'ri-eye-fill' : 'ri-eye-off-fill';
    });
}