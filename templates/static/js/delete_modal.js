const modalOverlay = document.getElementById('modal_overlay')
const notDelete = document.getElementById('not_delete')


const handleConfirm = () => {
    if (modalOverlay.style.display === '') {
        modalOverlay.style.display = 'flex'
    } else {
        modalOverlay.style.display = ""
    }
}

notDelete.addEventListener('click', () => {
    handleConfirm()
})

modalOverlay.addEventListener('click', function(e) {
    if (e.target === this) {
        handleConfirm()
    }
})
