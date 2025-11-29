// Contact Us carousel functionality
const $next = document.querySelector('.next');
const $prev = document.querySelector('.prev');
const $slide = document.querySelector('.slide');

// Check if elements exist before adding event listeners
if ($next && $prev && $slide) {
    $next.addEventListener('click', () => {
        const items = document.querySelectorAll('.item');
        if (items.length > 0) {
            $slide.appendChild(items[0]);
        }
    });

    $prev.addEventListener('click', () => {
        const items = document.querySelectorAll('.item');
        if (items.length > 0) {
            $slide.prepend(items[items.length - 1]);
        }
    });
}