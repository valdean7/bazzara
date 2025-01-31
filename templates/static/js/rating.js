document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('reviewForm');
    const modalOverlayRating = document.getElementById('modal_overlay_rating');
    const ratingContainer = document.getElementById('rating');
    const outlineStars = ratingContainer.querySelectorAll('.outline-star');
    const selectedRatingInput = document.getElementById('selectedRating');
    const ratingError = document.getElementById('ratingError');
    
    let selectedRating = 0;
    let currentHover = 0;

    const updateStars = () => {
        const activeRating = currentHover || selectedRating;
        outlineStars.forEach((star, index) => {
            star.classList.toggle('opacity-0', index >= activeRating);
            star.classList.toggle('opacity-100', index < activeRating);
        });
    };

    // Fechar modal ao clicar fora
    modalOverlayRating.addEventListener('click', function(e) {
        const display = modalOverlayRating.computedStyleMap().get('display')
        if (e.target === this) {
            if (display.value === 'flex') {
                modalOverlayRating.classList.replace('flex', 'hidden')
            }
        };
        
    });

    // Eventos de interação com as estrelas
    ratingContainer.addEventListener('mouseover', (e) => {
        const starButton = e.target.closest('.star-button');
        if (!starButton) return;
        
        currentHover = parseInt(starButton.dataset.rating, 10);
        updateStars();
    });

    ratingContainer.addEventListener('mouseleave', () => {
        currentHover = selectedRating;
        updateStars();
    });

    ratingContainer.addEventListener('click', (e) => {
        const starButton = e.target.closest('.star-button');
        if (!starButton) return;
        
        selectedRating = parseInt(starButton.dataset.rating, 10);
        selectedRatingInput.value = selectedRating;
        currentHover = selectedRating;
        updateStars();
        ratingError.classList.add('hidden');
    });

    // Validação do formulário
    form.addEventListener('submit', (e) => {
        if (selectedRating === 0) {
            e.preventDefault();
            ratingError.classList.remove('hidden');
            ratingContainer.focus();
            ratingContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    });

    // Acessibilidade com teclado
    ratingContainer.addEventListener('keydown', (e) => {
        const starButtons = Array.from(ratingContainer.querySelectorAll('.star-button'));
        const currentFocused = document.activeElement;
        const index = starButtons.indexOf(currentFocused);

        if (e.key === 'ArrowRight' && index < starButtons.length - 1) {
            starButtons[index + 1].focus();
        } else if (e.key === 'ArrowLeft' && index > 0) {
            starButtons[index - 1].focus();
        } else if (e.key === 'Enter' || e.key === ' ') {
            currentFocused.click();
        }
    });
});