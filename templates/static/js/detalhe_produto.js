const variantes = document.querySelectorAll('.img-size')
const especificacoesContainer = document.querySelector('.esp_container')
const produtoImagem = document.getElementById('produto_imagem')
const quantidadeContainer = document.getElementById('quant_container')
const incrementarBtn = document.getElementById('increment')
const decrementarBtn = document.getElementById('decrement')
const quantidadeInput = document.getElementById('quantidade')
const formulario = document.getElementById('produto_form')
const ratingContainer = document.getElementById('rating_container')
const starBtnContainer = document.getElementById('star_btn_container')


// tratamento das variações
const getImagemLink = (src) => {
    const mediaIndex = src.indexOf('/media')
    const imagemLink = src.slice(mediaIndex)
    return imagemLink
}

const changeProdutoImagem = (link) => {
    produtoImagem.setAttribute('src', link)
}

const toggleVariation = (targetElement) => {
    const input = document.getElementById('variante_nome')
    const inputId = document.getElementById('variante_id')
    const imagemInput = document.getElementById('imagem')
    const dataNome = targetElement.dataset.nome
    const dataId = targetElement.dataset.id
    variantes.forEach(variante => {
        const variantNode = variante.closest('.variant')
        if (! variantNode.isSameNode(targetElement)) {
            if (! variantNode.childNodes[3].classList.contains('hidden')) {
                variantNode.childNodes[3].classList.add('hidden')
            }
        }
    })
    const variacaoClasses = targetElement.querySelector('.checked')
    const variacaoImagem = targetElement.querySelector('img').src
    const mediaIndex = variacaoImagem.indexOf('/media')
    if (variacaoClasses.classList.contains('hidden')) {
        variacaoClasses.classList.remove('hidden')
        input.setAttribute('value', dataNome)
        inputId.setAttribute('value', dataId)
        imagemInput.setAttribute('value', variacaoImagem.slice(mediaIndex))
    } else {
        variacaoClasses.classList.add('hidden')
        input.setAttribute('value', "")
        inputId.setAttribute('value', "")
        imagemInput.setAttribute('value', "")
    }
}

const getCheckIcon = () => {
    const especificacao = document.querySelector('.esp_size')
    const checkIcon = especificacao.querySelector('.checked').cloneNode(true)
    if (! checkIcon.classList.contains('hidden')) {
        checkIcon.classList.add('hidden')
    }
    return checkIcon
}

const createEspecificationElement = (variantIndex) => {
    const varianteEspecificacoes = document.getElementById(`var_esp_${variantIndex}`)

    const varianteEspc = varianteEspecificacoes.querySelectorAll('p')

    const input = document.createElement('input')
    input.setAttribute('type', 'hidden')
    input.setAttribute('name', 'size')
    input.setAttribute('id', 'especificacao_tamanho')
    
    
    const arr = [input]
    varianteEspc.forEach(esp => {
        const data = esp.innerText.split('/')

        const div = document.createElement('div')
        div.classList.add('esp_size', 'variant')
        if (Number(data[1]) <= 0) {
            div.classList.add('pointer-events-none', 'opacity-40')
        }

        const span = document.createElement('span')
        span.classList.add('uppercase', 'w-fit', 'h-fit', 'select-none')
        span.innerText = data[0]

        div.appendChild(span)
        div.appendChild(getCheckIcon())

        arr.push(div)
    })
    return arr
}

const replaceSpecificationConteiner = (nodeElementList) => {
    const especificacoes = document.querySelectorAll('.esp_size')
    const parent = especificacoes[0].parentElement
    parent.replaceChildren(...nodeElementList)
}

variantes.forEach(variante => {
    variante.addEventListener('click', (e) => {
        
        toggleVariation(e.target.closest('.variant'))

        const varianteImagem = getImagemLink(e.target.src)
        changeProdutoImagem(varianteImagem)

        const variantIndex = e.target.id.slice(-1)
        
        const espList = createEspecificationElement(variantIndex)

        replaceSpecificationConteiner(espList)

    })

})

// tratamento das especificações
const getSpecificationPrice = (varIndex) => {
    const currentSpecificarion = document.getElementById(`var_esp_${varIndex}`)
    const data = currentSpecificarion.querySelectorAll('p')
    return data
}


const toggleSpecification = (targetElement) => {
    const input = document.getElementById('especificacao_tamanho')    
    const isSpecification = targetElement.classList.contains('esp_size')
    const checkIconElement = targetElement.querySelector('div')

    const allSpecification = especificacoesContainer.querySelectorAll('.esp_size')
    if (isSpecification) {
        allSpecification.forEach(esp => {
            if (! esp.isSameNode(targetElement)) {
                if (! esp.querySelector('div').classList.contains('hidden')) {
                    esp.querySelector('div').classList.add('hidden')
                }
            }
        })
    }
    if (isSpecification && checkIconElement.classList.contains('checked')) {
        const span = targetElement.querySelector('span')
        
        if (checkIconElement.classList.contains('hidden')) {
            checkIconElement.classList.remove('hidden')
            input.setAttribute('value', span.innerText)
        } else {
            checkIconElement.classList.add('hidden')
            input.setAttribute('value', "")
        }
    }
}


especificacoesContainer.addEventListener('click', (e) => {
    const specification = e.target.closest('div')
    
    toggleSpecification(specification)
})

// tratamento da quantidade
const estoque = +quantidadeContainer.dataset.estoque


incrementarBtn.addEventListener('click', () => {
    const inputValue = document.getElementById('quantidade')
    if (isNaN(inputValue.value)) return
    if (+inputValue.value < estoque) {
        inputValue.value = Number(inputValue.value) + 1
    }
})


decrementarBtn.addEventListener('click', () => {
    const inputValue = document.getElementById('quantidade')
    if (isNaN(inputValue.value) || +inputValue.value <= 1) return
    inputValue.value = Number(inputValue.value) - 1
})

quantidadeInput.addEventListener('input', (e) => {
    if (e.target.value === '0' && e.target.value.length === 1) {
        e.target.value = ''
    }
    const value = e.target.value.replace(/[^0-9]/g, '').slice(0,4)
    e.target.value = value
})


// tratamento do formulário

formulario.addEventListener('submit', (e) => {
    e.preventDefault()
    const modelo = document.getElementById('variante_nome').value
    const tamanho = document.getElementById('especificacao_tamanho').value
    const quantidade = document.getElementById('quantidade').value
    const imagem = document.getElementById('imagem').value

    if (modelo && tamanho && quantidade && imagem) {
        formulario.submit()
    }
})

const toggleComments = (star) => {
    const comments = ratingContainer.querySelectorAll('comment')
    comments.forEach(comment => {
        if (star === 'all') {
            if (comment.classList.contains('hidden')) {
                comment.classList.replace('hidden', 'flex')
            }
        } else  {
            if (comment.dataset.rating !== star) {
                if (comment.classList.contains('flex')) {
                    comment.classList.replace('flex', 'hidden')
                }
            }
            if (comment.dataset.rating === star) {
                if (comment.classList.contains('hidden')) {
                    comment.classList.replace('hidden', 'flex')
                }
            }
        }
        
    })
}


const starBtn = starBtnContainer.querySelectorAll('div')
starBtn.forEach(item => {
    item.addEventListener('click', function() {
        const star = this.dataset.star
        starBtn.forEach(btn => {
            if (this === btn) {
                btn.classList.add('btn_star_selected')
            } else {
                if (btn.classList.contains('btn_star_selected')) {
                    btn.classList.remove('btn_star_selected')
                }
            }
        })
        toggleComments(star)
    })
})
