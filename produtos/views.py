from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http.request import HttpRequest
from .models import Produto, Variacao, Especificacao
from utils.carrinho import (variacao_existe, aplicar_desconto, remover_produto,
                            pegar_produtos, produtos_preco_total)
from django.contrib import messages


def home(request: HttpRequest):
    produtos = Produto.objects.all()
    return render(request, 'home.html', {'produtos': produtos})


def detalhe_produto(request: HttpRequest, slug: str):
    produto = get_object_or_404(Produto, slug=slug)
    variacoes: list[Variacao] = produto.variacoes.all()

    estoque = sum(
        [e.estoque for v in variacoes for e in v.especificacoes.all()]
    )

    context = {
        'variacoes': variacoes, 
        'produto': produto, 
        'estoque': estoque,
    }
    return render(request, 'detalhe_produto.html', context)


def adicionar_no_carrinho(request: HttpRequest):
    if request.method == 'POST':
        produto_id = request.POST.get('product')
        produto_nome = request.POST.get('product_name')
        variacao_nome = request.POST.get('model')
        tamanho = request.POST.get('size')
        slug = request.POST.get('slug')
        imagem = request.POST.get('image')
        promocao = int(request.POST.get('promotion'))
        quantidade = int(request.POST.get('quant'))
        preco = float(request.POST.get('price').replace(',', '.'))

        http_referer = request.META.get('HTTP_REFERER', 
        reverse('produtos:produto',args=(slug,)))

        pro_existe = Produto.objects.filter(
        id=produto_id, nome=produto_nome, preco=preco).exists()

        var_existe = Variacao.objects.filter(
        produto_id=produto_id, nome_variacao=variacao_nome).exists()

        esp_existe = Especificacao.objects.filter(tamanho=tamanho,
        variacao__nome_variacao=variacao_nome).exists()

        if not pro_existe or not var_existe or not esp_existe:
            messages.error(request, 'Ouve uma falha ao adicionar o produto no  carrinho. Tente novamente.')
            return redirect(http_referer)
        
        if not request.session.get('carrinho'):
            request.session['carrinho'] = {}
            request.session.save()

        carrinho = request.session.get('carrinho', {})

        novo_produto = {
            'variacao_nome': variacao_nome,
            'produto_nome': produto_nome,
            'tamanho': tamanho,
            'quantidade': quantidade,
            'slug': slug,
            'preco': preco,
            'imagem': imagem,
            'preco_quantitativo': quantidade * preco,
            'promocao': promocao,
            'preco_promocional': aplicar_desconto((quantidade * preco), promocao)
        }

        if produto_id in carrinho:
            dados = {
                'variacao_nome': variacao_nome, 
                'tamanho': tamanho,
                'quantidade': quantidade,
                'preco': preco,
                'promocao': promocao,
            }

            existe, produtos = variacao_existe(carrinho[produto_id], dados)

            if existe:
                carrinho[produto_id] = produtos
            else:
                carrinho[produto_id].append(novo_produto)
                request.session['carrinho'] = carrinho

        else :
            carrinho[produto_id] = [novo_produto]

        request.session.save()
        messages.success(request, 'Produto adicionado no carrinho.')
        return redirect(http_referer)
    

def carrinho(request: HttpRequest):
    carrinho = request.session.get('carrinho', {})
    produtos = pegar_produtos(carrinho)
    total = produtos_preco_total(produtos)
    
    return render(request, 'carrinho.html', 
                {'produtos': produtos, 'total': total})


def remover_do_carrinho(request: HttpRequest):
    carrinho = request.session.get('carrinho', {})
    pro = request.GET.get('pro')
    var = request.GET.get('var')
    tamanho = request.GET.get('tamanho')
    produtos_atualizados = remover_produto(carrinho,pro, var, tamanho)
    request.session['carrinho'] = produtos_atualizados
    request.session.save()
    return redirect('produtos:carrinho')
