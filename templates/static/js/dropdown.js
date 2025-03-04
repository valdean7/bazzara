const perfil = document.getElementById('perfil')
const perfilDropdown = document.getElementById('perfil_dropdown')
let isHovered = false
let hasClicked = false


document.addEventListener('click', function(e) {
    if (!perfil.contains(e.target)) {
        hasClicked = false
        perfilDropdown.style.display = 'none'
    }
})

perfil.addEventListener('click', () => {
    if (hasClicked) {
        hasClicked = false
    } else {
        hasClicked = true
    }
})


perfil.addEventListener('mouseenter', () => {
    if (hasClicked) return
    perfilDropdown.style.display = 'block'
})

perfil.addEventListener('mouseleave', () => {
    if (hasClicked) return
    setTimeout(() => {
        if (! isHovered) {
            perfilDropdown.style.display = 'none'
        }
    }, 135)
})

perfilDropdown.addEventListener('mouseenter', () => {
    if (hasClicked) return
    isHovered = true
    perfilDropdown.style.display = 'block'
})

perfilDropdown.addEventListener('mouseleave', () => {
    if (hasClicked) return
    perfilDropdown.style.display = 'none'
    isHovered = false
})