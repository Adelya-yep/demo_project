let currentSlide = 0;
const slides = document.querySelectorAll('.slide');
const totalSlides = slides.length;
let autoSlideInterval;

function showSlide(index) {
    slides.forEach((slide, i) => {
        slide.classList.toggle('active', i === index);
    });
}

function nextSlide() {
    currentSlide = (currentSlide + 1) % totalSlides;
    showSlide(currentSlide);
    resetAutoSlide();
}

function prevSlide() {
    currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
    showSlide(currentSlide);
    resetAutoSlide();
}

function startAutoSlide() {
    autoSlideInterval = setInterval(nextSlide, 3000);
}

function resetAutoSlide() {
    clearInterval(autoSlideInterval);
    startAutoSlide();
}

function maskPhone(input) {
    let digits = input.value.replace(/\D/g, '');
    if (input.value.startsWith('8')) {
        digits = '7' + digits.slice(1);
    }
    if (digits.length === 0) {
        input.value = '';
        return;
    }
    let formatted = '+7';
    if (digits.length > 1) {
        formatted += ' (' + digits.slice(1, 4);
    }
    if (digits.length >= 5) {
        formatted += ') ' + digits.slice(4, 7);
    }
    if (digits.length >= 8) {
        formatted += '-' + digits.slice(7, 9);
    }
    if (digits.length >= 10) {
        formatted += '-' + digits.slice(9, 11);
    }
    input.value = formatted;
    if (digits.length > 11) {
        input.value = input.value.slice(0, 18);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    if (slides.length > 0) {
        showSlide(0);
        startAutoSlide();
    }

    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert-dismissible');
        alerts.forEach(function(alert) {
            let bsAlert = new bootstrap.Alert(alert);
            setTimeout(function() {
                bsAlert.close();
            }, 5000);
        });
    }, 100);

    const phoneInput = document.getElementById('id_phone');
    if (phoneInput) {
        phoneInput.addEventListener('input', function() {
            maskPhone(this);
        });
        phoneInput.setAttribute('maxlength', '18');
    }
});
