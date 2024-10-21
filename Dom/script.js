function toggleTheme() {
    const body = document.body;
    const header = document.querySelector('header');
    const nav = document.querySelector('nav');
    const sections = document.querySelectorAll('.section');
    const footer = document.querySelector('footer');
    const themeButton = document.getElementById('themeToggleButton');

    body.classList.toggle('dark-mode');
    header.classList.toggle('dark-mode');
    nav.classList.toggle('dark-mode');
    sections.forEach(section => section.classList.toggle('dark-mode'));
    footer.classList.toggle('dark-mode');

    if (body.classList.contains('dark-mode')) {
        themeButton.textContent = "🌙";
    } else {
        themeButton.textContent = "☀️";
    }
}

document.getElementById('themeToggleButton').addEventListener('click', toggleTheme);
