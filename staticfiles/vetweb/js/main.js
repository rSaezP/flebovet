// Para validación de formularios
document.addEventListener('DOMContentLoaded', function() {
    // Validación de formulario de registro
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', validateForm);
    }

    // Filtros dinámicos de productos
    const filterInputs = document.querySelectorAll('.filter-input');
    filterInputs.forEach(input => {
        input.addEventListener('change', filterProducts);
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const slides = document.querySelectorAll('.slideshow__slide');
    let currentSlide = 0;

    function nextSlide() {
        slides[currentSlide].classList.remove('active');
        currentSlide = (currentSlide + 1) % slides.length;
        slides[currentSlide].classList.add('active');
    }

    setInterval(nextSlide, 5000); // Cambia cada 5 segundos
});




    const navbar = document.querySelector('.navbar');
    const navbarBrand = document.querySelector('.navbar-brand');

    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
            navbarBrand.style.visibility = 'hidden';
            navbarBrand.style.opacity = '0';
        } else {
            navbar.classList.remove('scrolled');
            navbarBrand.style.visibility = 'visible';
            navbarBrand.style.opacity = '1';
        }
    });
