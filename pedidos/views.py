from django.shortcuts import render, redirect
from django.http import HttpRequest
from endereco.models import Endereco
from utils.carrinho import (pegar_produtos, produtos_preco_total,
                            editar_produtos)
from payment_emulation.payment.paymentSDK import PaymentSDK
from utils.decorators import login_required_warning
import json


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


def efetuar_pagamento(request: HttpRequest):
    carrinho = request.session.get('carrinho', {})
    seed = PaymentSDK.get_seeds()['PROBATUS']
    cpf = seed['account'].get('cpf')
    card_number = seed['card'].get('card_number')
    cvv = seed['card'].get('cvv')
    validity = seed['card'].get('validity')
    holder = seed['card'].get('card_holder_name')

    produtos = pegar_produtos(carrinho)
    itens = editar_produtos(produtos)

    sdk = PaymentSDK(itens)
    response = sdk.payment(cpf,card_number,validity, cvv, holder)
    res_json = json.loads(response)
    if res_json['transaction'] == 'success':
        del request.session['carrinho']
    return redirect('pedidos:pagar_pedidos')
