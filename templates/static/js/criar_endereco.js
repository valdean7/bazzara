const estatdoSelector = document.getElementById('estado')
const cidadeSelector = document.getElementById('cidade')
const nomeInput = document.getElementById('nome_completo')
const telefoneInput = document.getElementById('telefone')
const cepInput = document.getElementById('cep')
const checkBoxNumero = document.getElementById('cb_numero')
const numeroInput = document.getElementById('numero')
const checkBoxControler = document.getElementById('cb_controler')


// adicionando estados
const ufUrl = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados?orderBy=nome'

async function getUF() {
    const response = await fetch(ufUrl)
    const data = await response.json()
    data.map((item) => {
        
        const option = document.createElement('option')
        option.text = item.nome 
        option.value = item.sigla
        if (estatdoSelector.dataset.estado) {
            if (estatdoSelector.dataset.estado === item.sigla) {
                option.selected = true 
            }
        } 
        estatdoSelector.append(option)
        
    })
    
    if (cidadeSelector.childNodes.length <= 2) {
        const uf = estatdoSelector.value
        getMunicipios(uf)
    }
}

getUF()

async function getMunicipios(UF) {
    const url = `https://servicodados.ibge.gov.br/api/v1/localidades/estados/${UF}/municipios`
    const response = await fetch(url)
    const data = await response.json()

    const cidadeOption = cidadeSelector.querySelectorAll('option')
    cidadeOption.forEach(option => {
        if (!option.disabled) option.remove()
    })

    data.map(item => {
        const option = document.createElement('option')
        option.text = item.nome 
        option.value = item.nome
        if (cidadeSelector.dataset.cidade) {
            if (cidadeSelector.dataset.cidade === item.nome) {
                option.selected = true
            }
        }
        cidadeSelector.append(option)
    })
}


// adicionando cidades
estatdoSelector.addEventListener('change', function() {
    const uf = estatdoSelector.value
    cidadeSelector.disabled = false
    getMunicipios(uf)
})


// _________________________________________________ //
telefoneInput.addEventListener('input', (e) => {
    const inputValue = e.target.value.replace(/[^0-9]/g, '').slice(0, 11)
    e.target.value = inputValue
})

cepInput.addEventListener('input', (e) => {
    const inputValue = e.target.value.replace(/[^0-9]/g, '').slice(0, 8)
    e.target.value = inputValue
})


nomeInput.addEventListener('input', (e) => {
    const inputValue = e.target.value.replace(/[^a-zA-ZÀ-ÿ\s]/g, '')
    e.target.value = inputValue
})

checkBoxNumero.addEventListener('change', (e) => {
    if (e.target.checked) {
        numeroInput.setAttribute('readonly', '')
        numeroInput.value = 's/n'
    } else {
        numeroInput.removeAttribute('readonly')
        numeroInput.value = ''
    }
})

if (numeroInput.value > 0) checkBoxControler.style.display = 'none'
numeroInput.addEventListener('input', (e) => {
    const inputValue = e.target.value.replace(/[^0-9]/g, '')
    e.target.value = inputValue
    
    if (e.target.value.length > 0) {
        checkBoxControler.style.display = 'none'        
    } else {
        checkBoxControler.style.display = 'flex'
    }
})
