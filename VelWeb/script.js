// script.js
const toggleBtn = document.getElementById("themeToggle");

toggleBtn.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
});

// Theme toggle logic with persistence
const themeToggleBtn = document.getElementById('themeToggle');
const currentTheme = localStorage.getItem('theme');

// Apply saved theme on load
if (currentTheme === 'dark') {
    document.body.classList.add('dark-theme');
}

// Toggle theme on button click
themeToggleBtn.addEventListener('click', () => {
    document.body.classList.toggle('dark-theme');

    // Save preference to localStorage
    if (document.body.classList.contains('dark-theme')) {
        localStorage.setItem('theme', 'dark');
    } else {
        localStorage.setItem('theme', 'light');
    }
});
    const slider = document.getElementById('slider');
    const panels = document.querySelectorAll('.panel');
    let index = 0;

    function updatePanels() {
        panels.forEach((panel, i) => {
        panel.classList.toggle('active', i === index);
    });
      slider.style.transform = `translateX(-${index * 100}%)`;
    }

    function nextSlide() {
        index = (index + 1) % panels.length;
        updatePanels();
    }

    function prevSlide() {
        index = (index - 1 + panels.length) % panels.length;
        updatePanels();
    } 
    