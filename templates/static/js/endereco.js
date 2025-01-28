const meuTelefone = document.getElementById('meu_telefone')
const meuCep = document.getElementById('meu_cep')


function setTelefone() {
    if (! meuTelefone.dataset.telefone) return
    const ddd = meuTelefone.dataset.telefone.slice(0,2)
    const numero1 = meuTelefone.dataset.telefone.slice(2, 7)
    const numero2 = meuTelefone.dataset.telefone.slice(7)
    meuTelefone.innerText = `(${ddd}) ${numero1}-${numero2}`
}

function setCep() {
    if (! meuCep.dataset.cep) return
    const cep1 = meuCep.dataset.cep.slice(0,5)
    const cep2 = meuCep.dataset.cep.slice(5)
    meuCep.innerText = `${cep1}-${cep2}`
}

setTelefone()
setCep()
