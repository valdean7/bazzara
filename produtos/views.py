from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from pedidos.models import Pedido
from utils.carrinho import (
    aplicar_desconto,
    pegar_produtos,
    preco_quant,
    produtos_preco_total,
    remover_produto,
    variacao_existe,
)

from .models import Avaliacao, Especificacao, Produto, Variacao

# from django.db import connection


def home(request: HttpRequest):
    produtos = Produto.objects.all().order_by('-id')
    # del request.session['carrinho']
    # with connection.cursor() as cursor:
    #     cursor.execute('DELETE FROM produtos_avaliacao WHERE id = "1";')
    # print(request.session['carrinho'])
    return render(request, 'home.html', {'produtos': produtos})


def busca(request: HttpRequest):
    search = request.GET.get('search')
    produtos = Produto.objects.filter(
        Q(nome__icontains=search)|
        Q(slug__icontains=search)
        # Q(categoria__nome_categoria__icontains=search)
    )
    return render(request, 'home.html', {'produtos': produtos})


def detalhe_produto(request: HttpRequest, slug: str):
    produto = get_object_or_404(Produto, slug=slug)
    variacoes: list[Variacao] = produto.variacoes.all()
    avaliacoes = Avaliacao.objects.filter(produto_id=produto.id)
    estoque = sum(
        [e.estoque for v in variacoes for e in v.especificacoes.all()]
    )

    context = {
        'variacoes': variacoes, 
        'produto': produto, 
        'estoque': estoque,
        'avaliacoes': avaliacoes,
    }
    return render(request, 'detalhe_produto.html', context)


def adicionar_no_carrinho(request: HttpRequest):
    if request.method == 'POST':
        produto_id = request.POST.get('product')
        produto_nome = request.POST.get('product_name')
        variacao_nome = request.POST.get('model')
        variacao_id = request.POST.get('variant_id')
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
            produto_id=produto_id, nome_variacao=variacao_nome, id=variacao_id
        ).exists()

        esp_existe = Especificacao.objects.filter(tamanho=tamanho,
        variacao__nome_variacao=variacao_nome).exists()

        if not pro_existe or not var_existe or not esp_existe:
            messages.error(request, 'Houve uma falha ao adicionar o produto no  carrinho. Tente novamente.')
            return redirect(http_referer)
        
        if not request.session.get('carrinho'):
            request.session['carrinho'] = {}
            request.session.save()

        carrinho = request.session.get('carrinho', {})

        novo_produto = {
            'variacao_nome': variacao_nome,
            'variacao_id': variacao_id,
            'produto_nome': produto_nome,
            'tamanho': tamanho,
            'quantidade': quantidade,
            'slug': slug,
            'preco': preco,
            'imagem': imagem,
            'promocao': promocao,
        }

        if produto_id in carrinho:
            dados = {
                'variacao_nome': variacao_nome,
                'variacao_id': variacao_id,
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
    # print(carrinho)
    produtos = pegar_produtos(carrinho)
    total = produtos_preco_total(produtos)
    
    return render(request, 'carrinho.html', 
                {'produtos': produtos, 'total': total})


def remover_do_carrinho(request: HttpRequest):
    carrinho = request.session.get('carrinho', {})
    # print(carrinho)
    pro = request.GET.get('pro')
    var = request.GET.get('var')
    var_id = request.GET.get('var_id')
    tamanho = request.GET.get('tamanho')
    produtos_atualizados = remover_produto(carrinho,pro, var, tamanho, var_id)
    request.session['carrinho'] = produtos_atualizados
    request.session.save()
    return redirect('produtos:carrinho')


@login_required(login_url='/registro')
def produto_avaliacao(request: HttpRequest, id):
    http_referer = request.META.get('HTTP_REFERER')
    if '/pedidos/todos' in http_referer:
        request.session['temp_url'] = reverse('pedidos:pedidos')
    elif '/pedidos/finalizados':
        request.session['temp_url'] = reverse('pedidos:finalizados')
    
    request.session.modified = True

    pedido = get_object_or_404(Pedido, id=id)
    nome_variacao = pedido.variacao_nome
    variacao = pedido.produto.variacoes.filter(
        nome_variacao=nome_variacao).first()
    context = {'pedido': pedido, 'variacao': variacao}
    return render(request, 'produto_avaliacao.html', context)


@login_required(login_url='/registro')
def avaliar(request: HttpRequest, uuid):
    if request.method == 'POST':
        
        avaliacao = int(request.POST.get('rating'))
        comentario = request.POST.get('comment')
        variacao_nome = request.POST.get('variation')
        pedido = request.POST.get('pedido')
        produto = get_object_or_404(Produto, id=uuid)
        try:
            Avaliacao.objects.create(
                produto=produto,
                pedido_id=pedido,
                variacao_nome=variacao_nome,
                avaliador=request.user,
                comentario=comentario,
                avaliacao=avaliacao
            )
        except:
            messages.error(request, 'Hove um erro ao avaliar o produto.')
        finally:
            redirect_url = request.session.get('temp_url')
            del request.session['temp_url']
            return redirect(redirect_url)


def produtos_em_promocao(request):
    produtos = Produto.objects.filter(promocao__gt=0)

    return render(request, 'home.html', {'produtos': produtos})


def produtos_blusas(request):
    produtos = Produto.objects.filter(
        categoria__nome_categoria__iexact='blusas'
    )

    return render(request, 'home.html', {'produtos': produtos})


def produtos_camisas(request):
    produtos = Produto.objects.filter(
        categoria__nome_categoria__iexact='camisas'
    )

    return render(request, 'home.html', {'produtos': produtos})


def produtos_calcados(request):
    produtos = Produto.objects.filter(
        categoria__nome_categoria__iexact='calçados'
    )

    return render(request, 'home.html', {'produtos': produtos})


def produtos_calsas(request):
    produtos = Produto.objects.filter(
        categoria__nome_categoria__iexact='calsas'
    )

    return render(request, 'home.html', {'produtos': produtos})


def produtos_shorts(request):
    produtos = Produto.objects.filter(
        categoria__nome_categoria__iexact='shorts'
    )

    return render(request, 'home.html', {'produtos': produtos})