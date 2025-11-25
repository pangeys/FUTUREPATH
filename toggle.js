const input = document.getElementById('Password');
const toggle = document.getElementById('togglePassword');

toggle.addEventListener('click',
    () => {
        const isPassword = input.type === 'password';
        input.type = isPassword ? 'text' : 'password';
        toggle.className = isPassword ? 'ri-eye-fill' 
        : 'ri-eye-off-fill';
    }
);