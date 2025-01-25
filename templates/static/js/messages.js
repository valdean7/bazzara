// const messageContainer = document.querySelector('message-container')
const messages = document.querySelectorAll('.alert')
const closeBtn = document.querySelectorAll('.close-btn')


messages.forEach(message => {
    setTimeout(() => {
        message.style.display = 'none'
    }, 13000)
})


closeBtn.forEach(btn => {
    btn.addEventListener('click', () => {
        btn.parentElement.style.display = 'none'
    })
})