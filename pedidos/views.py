from django.shortcuts import render, redirect
from django.http import HttpRequest
from endereco.models import Endereco
from django.contrib.auth.decorators import login_required
from utils.carrinho import (pegar_produtos, produtos_preco_total,
                            editar_produtos)
from payment_emulation.payment.paymentSDK import PaymentSDK
from utils.decorators import login_required_warning
import json
from pedidos.models import Pedido
from produtos.models import Avaliacao, Especificacao
from utils.pedidos import criar_pedidos
from django.contrib import messages


@login_required_warning(redirect_url='registro:registrar')
def pagar_pedidos(request: HttpRequest):
    carrinho = request.session.get('carrinho', {})
    if len(carrinho) == 0:
        return redirect('produtos:home')
    endereco = Endereco.objects.filter(usuario=request.user).first()
    produtos = pegar_produtos(carrinho)
    total = produtos_preco_total(produtos)

    context = {'endereco': endereco, 'produtos': produtos, 'total': total}
    return render(request, 'pagar_pedidos.html', context)


@login_required(login_url='/registro')
def efetuar_pagamento(request: HttpRequest):
    carrinho = request.session.get('carrinho', {})
    seed = PaymentSDK.get_seeds()['PROBATUS']
    cpf = seed['account'].get('cpf')
    card_number = seed['card'].get('card_number')
    cvv = seed['card'].get('cvv')
    validity = seed['card'].get('validity')
    holder = seed['card'].get('card_holder_name')

    produtos = pegar_produtos(carrinho)
    print(produtos)
    itens = editar_produtos(produtos)

    sdk = PaymentSDK(itens)
    response = sdk.payment(card_number,validity, cvv, holder, cpf)

    res_json = json.loads(response)
    # TODO: deletar a session no final
    del request.session['carrinho']
    pedidos = criar_pedidos(request, res_json)
    Pedido.objects.bulk_create([Pedido(**pedido) for pedido in pedidos])

    match res_json['transaction']:
        case 'success':
            especificacoes = []
            for produto in produtos:
                especificacao = Especificacao.objects.filter(
                    variacao_id=produto['variacao_id'],
                    tamanho=produto['tamanho'],
                ).first()
                especificacao.estoque = (
                    especificacao.estoque - produto['quantidade']
                )
                especificacoes.append(especificacao)

            Especificacao.objects.bulk_update(especificacoes, ['estoque'])

            messages.success(request, 'Pagamento efetuado com sucesso.')
            return redirect('pedidos:pedidos')
        case 'failure':
            messages.error(request, 'Houve uma falha ao efetuar o pagamento.')
            return redirect('pedidos:pedidos')
        case 'pending':
            messages.warning(request, 'O pagamento da compra está pendente.')
            return redirect('pedidos:pedidos')


@login_required(login_url='/registro')
def meus_pedidos(request: HttpRequest):
    pedidos = Pedido.objects.filter(comprador=request.user).order_by('-id')
    avaliacoes_ids = [
        a.pedido.pk
        for a in Avaliacao.objects.filter(avaliador=request.user)
    ]
    context = {'pedidos': pedidos, 'avaliacoes_ids': avaliacoes_ids}
    return render(request, 'pedidos.html', context)


@login_required(login_url='/registro')
def meus_pedidos_a_pagar(request: HttpRequest):
    pedidos = Pedido.objects.filter(
        comprador=request.user, status='PD').order_by('-id')
    return render(request, 'pedidos.html', {'pedidos': pedidos})


@login_required(login_url='/registro')
def cancelar_pedido(request: HttpRequest, id):
    if pedido := Pedido.objects.filter(comprador=request.user, pk=id).first():
        pedido.status = 'CL'
        try:
            pedido.save()
            messages.success(request, 'O pedido foi cancelado.')
        except:
            messages.error(request, 'Houve um erro ao cancelar o pedido.')
        finally:
            return redirect('pedidos:pedidos')
    else:
        messages.error(request, 'Houve um erro ao cancelar o pedido.')
        return redirect('pedidos:pedidos')


@login_required(login_url='/registro')
def pedidos_cancelados(request: HttpRequest):
    pedidos = Pedido.objects.filter(
        comprador=request.user, status='CL').order_by('-id')
    return render(request, 'pedidos.html', {'pedidos': pedidos})


@login_required(login_url='/registro')
def pedidos_finalizados(request: HttpRequest):
    pedidos = Pedido.objects.filter(
        comprador=request.user, status='PG').order_by('-id')
    avaliacoes_ids = [
        a.pedido.pk
        for a in Avaliacao.objects.filter(avaliador=request.user)
    ]
    context = {'pedidos': pedidos, 'avaliacoes_ids': avaliacoes_ids}
    return render(request, 'pedidos.html', context)


@login_required(login_url='/registro')
def devolver_pedido(request: HttpRequest, id):
    if pedido := Pedido.objects.filter(comprador=request.user, pk=id).first():
        pedido.status = 'DV'
        try:
            pedido.save()
            messages.success(request, 'O pedido foi devolvido.')
        except:
            messages.error(request, 'Houve um erro ao devolvido o pedido.')
        finally:
            return redirect('pedidos:pedidos')
    else:
        messages.error(request, 'Houve um erro ao devolvido o pedido.')
        return redirect('pedidos:pedidos')


@login_required(login_url='/registro')
def pedidos_devolvidos(request: HttpRequest):
    pedidos = Pedido.objects.filter(
        comprador=request.user, status='DV').order_by('-id')
    return render(request, 'pedidos.html', {'pedidos': pedidos})
