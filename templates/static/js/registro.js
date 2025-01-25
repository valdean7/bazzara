const showPasswordLogin = document.getElementById('show_password_login')
const showPasswordRegister = document.getElementById('show_password_register')
const passwordLoginInput = document.getElementById('passwordd')
const passwordRegisterInput = document.getElementById('password')


const toggleShowPassword = (e, inputPassword) => {
    if (e.target.src.includes('eye-on.svg')) {
        const newSrc = e.target.src.replace('eye-on.svg', 'eye-off.svg')
        e.target.src = newSrc
        inputPassword.setAttribute('type', 'text')
    } else {
        const newSrc = e.target.src.replace('eye-off.svg', 'eye-on.svg')
        e.target.src = newSrc
        inputPassword.setAttribute('type', 'password')
    }
}

showPasswordLogin.addEventListener('click', (e) => {
    toggleShowPassword(e, passwordLoginInput) 
})

showPasswordRegister.addEventListener('click', (e) => {
    toggleShowPassword(e, passwordRegisterInput)
})
